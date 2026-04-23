#!/usr/bin/env python3
"""CLI for Visual–Acoustic Tap Model

Supports:
- simulation mode (dimensions + source pos) -> prints reflections + modal peaks
- --from-wav path -> analyze tap WAV and estimate spike times
- optional --save-json to persist a small report
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from acoustics.tap_model import Room, Source, build_report, detect_spikes_from_wav

# CLI entrypoint note: mark script executable on Unix-like systems if needed


def main(argv=None):
    p = argparse.ArgumentParser(prog='tap_report')
    p.add_argument('--length', type=float, default=5.0, help='Room length (m)')
    p.add_argument('--width', type=float, default=4.0, help='Room width (m)')
    p.add_argument('--height', type=float, default=3.0, help='Room height (m)')
    p.add_argument('--source', type=float, nargs=3, metavar=('X','Y','Z'), default=None, help='Source position (m)')
    p.add_argument('--tap-energy', type=float, default=1.0, help='Relative tap energy')
    p.add_argument('--from-wav', type=str, default=None, help='Analyze recorded tap (wav)')
    p.add_argument('--peak-prominence', type=float, default=0.05, help='Peak prominence for detection')
    p.add_argument('--save-json', type=str, default=None, help='Save report to JSON file')

    args = p.parse_args(argv)

    room = Room(args.length, args.width, args.height)
    if args.source:
        sx, sy, sz = args.source
        source = Source(sx, sy, sz)
    else:
        source = Source(args.length / 2.0, args.width / 2.0, args.height / 2.0)

    report = build_report(room, source, tap_energy=args.tap_energy)

    if args.from_wav:
        path = Path(args.from_wav)
        if not path.exists():
            print(f"File not found: {path}")
            sys.exit(2)
        try:
            spikes = detect_spikes_from_wav(str(path), window_ms=200.0, peak_prominence=args.peak_prominence)
        except RuntimeError as e:
            print(f"Audio dependencies missing or failed: {e}")
            sys.exit(3)
        report['measured_spikes'] = [{'time_s': t, 'amp': a} for t, a in spikes]

    # Pretty print main findings
    print('Room:', report['room'])
    print('\nReflections (early):')
    for r in report['reflections']:
        print(f" - {r['surface']}: t={r['time_s']*1000:.1f} ms, amp={r['amp']:.4f}")

    if 'measured_spikes' in report:
        print('\nMeasured spikes (from WAV, first 200 ms):')
        for s in report['measured_spikes']:
            print(f" - t={s['time_s']*1000:.1f} ms, amp={s['amp']:.3f}")

    print('\nModal peaks (lowest):')
    for m in report['modes'][:10]:
        print(f" - mode={m['mode']} f={m['freq_hz']:.1f} Hz")

    if args.save_json:
        Path(args.save_json).write_text(json.dumps(report, indent=2))
        print(f"Saved report to {args.save_json}")


if __name__ == '__main__':
    main()
