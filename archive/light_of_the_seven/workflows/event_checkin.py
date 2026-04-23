from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FLOORS: dict[str, str] = {
    "basement": "Basement · Registry (sign-in/out, continuity)",
    "2": "2nd Floor · Research Lab (experiments, exploration)",
    "4": "4th Floor · Documentation & Onboarding",
    "7": "7th Floor · Governance & Canon",
    "8": "8th Floor · Quality & Workflows",
    "16": "16th Floor · Core Runtime (grid/circuits)",
}


@dataclass(frozen=True)
class EventEntry:
    schema: str
    created_at: str
    action: str
    name: str
    floor: str
    floor_label: str
    intent: str
    energy: str | None = None
    notes: str | None = None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _append_jsonl(path: Path, record: dict[str, Any]) -> None:
    _ensure_parent(path)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _tail_jsonl(path: Path, n: int) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    return lines[-n:]


def _prompt(msg: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{msg}{suffix}: ").strip()
    return value or (default or "")


def _normalize_floor(floor: str) -> str:
    f = floor.strip().lower()
    if f in ("b", "basement", "base"):
        return "basement"
    if f in ("2", "4", "7", "8", "16"):
        return f
    return f


def main() -> int:
    parser = argparse.ArgumentParser(description="GRID Workspace Event Check-In")
    parser.add_argument("--mode", choices=["check_in", "check_out", "tail"], default="check_in")
    parser.add_argument("--name", default="")
    parser.add_argument("--floor", default="")
    parser.add_argument("--intent", default="")
    parser.add_argument("--energy", default="")
    parser.add_argument("--notes", default="")
    parser.add_argument("--n", type=int, default=12, help="Number of recent entries for tail mode")

    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    log_path = repo_root / "logs" / "sessions" / "checkins.jsonl"

    if args.mode == "tail":
        lines = _tail_jsonl(log_path, args.n)
        if not lines:
            print(f"(no entries yet) {log_path}")
            return 0
        for line in lines:
            print(line)
        return 0

    name = args.name.strip() or _prompt("Name")
    floor = _normalize_floor(args.floor.strip() or _prompt("Floor (basement/2/4/7/8/16)", "basement"))
    floor_label = FLOORS.get(floor, floor)
    intent = args.intent.strip() or _prompt("Intent (1 sentence)")
    energy = args.energy.strip() or _prompt("Energy (low/medium/high)", "medium")
    notes = args.notes.strip() or ""

    entry = EventEntry(
        schema="grid.event_checkin.v1",
        created_at=_now_iso(),
        action=args.mode,
        name=name,
        floor=floor,
        floor_label=floor_label,
        intent=intent,
        energy=energy or None,
        notes=notes or None,
    )

    _append_jsonl(log_path, asdict(entry))

    today_path = repo_root / "workflows" / "TODAY.md"
    print("\n✅ logged")
    print(f"- file: {log_path}")
    print(f"- action: {entry.action}")
    print(f"- floor: {entry.floor_label}")
    print(f"- next: open {today_path} and add ONE checkbox item (keep it tiny)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
