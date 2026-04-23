#!/usr/bin/env bash
# Step 9 — cold start wall times; p95 over LO7_BENCH_RUNS (default 5).
# Prefers release Rust/Go when present. See tools/octopus/BENCHMARK.md.
# Does not set LO7_DEFAULT (step 10).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
CFG="${1:-lo7_corpus.test.yaml}"
REF="${2:-2019-02-15}"
RUNS="${LO7_BENCH_RUNS:-5}"

RUST_REL="$ROOT/prototype/rust/target/release/lo7-manifest-service"
RUST_DBG="$ROOT/prototype/rust/target/debug/lo7-manifest-service"
if [[ -n "${LO7_RUST_BIN:-}" ]]; then
  RUST_BIN="$LO7_RUST_BIN"
elif [[ -x "$RUST_REL" ]]; then
  RUST_BIN="$RUST_REL"
else
  RUST_BIN="$RUST_DBG"
fi

if [[ -n "${LO7_GO_BIN:-}" ]]; then
  GOX="$LO7_GO_BIN"
elif [[ -x /tmp/lo7-go-release ]]; then
  GOX="/tmp/lo7-go-release"
else
  GOX="/tmp/lo7-go"
fi

if [[ ! -f $ROOT/tools/octopus/BENCHMARK.md ]]; then
  echo "ERROR: tools/octopus/BENCHMARK.md must exist (step 7) before first benchmark (step 9)." >&2
  exit 1
fi

# One timing in seconds per line. LO7_BENCH_PRECISE=1 uses time.perf_counter (sub-millisecond for tiny work).
run_cold_lines() {
  local i tmp
  for ((i = 0; i < RUNS; i++)); do
    if [[ -n ${LO7_BENCH_PRECISE:-} ]]; then
      python3 -c "
import subprocess, sys, time
a = list(sys.argv[1:])
t0 = time.perf_counter()
r = subprocess.run(a)
if r.returncode:
    raise SystemExit(r.returncode)
print(f\"{time.perf_counter() - t0:.6f}\")
" "$@" || return 1
    else
      tmp=$(mktemp)
      if ! /usr/bin/env time -f "%e" -o "$tmp" "$@"; then
        rm -f "$tmp"
        return 1
      fi
      tr -d '\n' <"$tmp"
      echo
      rm -f "$tmp"
    fi
  done
}

p95() {
  python3 -c "
import math, sys
a = sorted(float(x) for x in sys.argv[1:] if x.strip())
if not a:
    print('0.0000')
    sys.exit(0)
k = min(len(a) - 1, max(0, math.ceil(0.95 * len(a)) - 1))
print(f\"{a[k]:.4f}\")
" "$@"
}

size_bytes() {
  if [[ -f "$1" ]]; then
    stat -c%s "$1" 2>/dev/null || wc -c <"$1" | tr -d ' '
  else
    echo 0
  fi
}

echo "================================================================"
echo "Lo7 benchmark  config=$CFG  ref=$REF  runs_per_impl=$RUNS"
echo "Rust: $RUST_BIN"
echo "Go:   $GOX"
echo "================================================================"
echo

echo "--- Python (uv run lo7-manifest) ---"
if mapfile -t SECS < <(run_cold_lines uv run lo7-manifest --config "$CFG" --ref-date "$REF" --out /tmp/lo7_bench_py.json); then
  P=$(p95 "${SECS[@]}")
  echo "  wall_sec_each: ${SECS[*]}"
  echo "  p95_wall_sec:  $P  (n=${#SECS[@]})"
  echo "  (interpreter/venv; no single static binary size for Python path)"
else
  echo "  (failed)"
fi
echo

echo "--- Rust ---"
if [[ -x $RUST_BIN ]]; then
  if mapfile -t SECS < <(run_cold_lines "$RUST_BIN" --config "$ROOT/$CFG" --ref-date "$REF" --out /tmp/lo7_bench_rs.json); then
    P=$(p95 "${SECS[@]}")
    echo "  wall_sec_each: ${SECS[*]}"
    echo "  p95_wall_sec:  $P  (n=${#SECS[@]})"
    echo "  size_bytes:     $(size_bytes "$RUST_BIN")"
  else
    echo "  (failed)"
  fi
else
  echo "  skip: $RUST_BIN not executable; cd prototype/rust && cargo build --release -p lo7-manifest-service"
fi
echo

echo "--- Go ---"
if [[ -x $GOX ]]; then
  if mapfile -t SECS < <(run_cold_lines "$GOX" --config "$ROOT/$CFG" --ref-date "$REF" --out /tmp/lo7_bench_go.json); then
    P=$(p95 "${SECS[@]}")
    echo "  wall_sec_each: ${SECS[*]}"
    echo "  p95_wall_sec:  $P  (n=${#SECS[@]})"
    echo "  size_bytes:     $(size_bytes "$GOX")"
  else
    echo "  (failed)"
  fi
else
  echo "  skip: $GOX not executable; cd prototype/go/lo7_manifest_service && go build -ldflags='-s -w' -o /tmp/lo7-go-release ."
fi
echo
echo "Done. Apply BENCHMARK.md (p95, then size, then tie order), set LO7_DEFAULT_MANIFEST_SERVICE (step 10)."
