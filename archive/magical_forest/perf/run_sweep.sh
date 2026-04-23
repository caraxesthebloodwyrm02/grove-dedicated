#!/usr/bin/env bash
set -euo pipefail

# perf/run_sweep.sh
# Simple runner for spectrum sweep with a SIMULATE mode.
# Usage: SIMULATE=1 ./perf/run_sweep.sh   # dry-run with simulated CSV rows
#        ./perf/run_sweep.sh              # run (requires wrk, cargo)

OUT_DIR="perf/results"
LOG_DIR="perf/logs"
PID_DIR="perf/pids"
mkdir -p "$OUT_DIR" "$LOG_DIR" "$PID_DIR"

ALL_CSV="$OUT_DIR/all_runs.csv"
if [ ! -f "$ALL_CSV" ]; then
  echo "run_id,build_mode,concurrency,input_size,repeat,duration_s,throughput_rps,p50_ms,p95_ms,p99_ms,error_rate,cpu_pct,rss_kb,notes,timestamp" > "$ALL_CSV"
fi

# Configuration - modify as needed
SERVER_CMD_DEFAULT="./target/release/magical_forest"
ENDPOINT="http://127.0.0.1:8080/"    # adjust to your app
DURATION=30
REPEATS=5
CONCURRENCY=(1 4 8 16)
INPUT_SIZES=(small medium large)
BUILDS=(release release-lto)

simulate=${SIMULATE:-0}

timestamp() { date -u +%Y-%m-%dT%H:%M:%SZ; }

for build in "${BUILDS[@]}"; do
  echo "--- build: $build"

  # Build step
  if [ "$simulate" = "1" ]; then
    echo "SIMULATE: build $build"
  else
    if [ "$build" = "release" ]; then
      echo "cargo build --release"
      cargo build --release
    else
      echo "RUSTFLAGS=\"-C lto -C codegen-units=1\" cargo build --release"
      RUSTFLAGS="-C lto -C codegen-units=1" cargo build --release
    fi
  fi

  for input_size in "${INPUT_SIZES[@]}"; do
    for c in "${CONCURRENCY[@]}"; do
      for rep in $(seq 1 $REPEATS); do
        run_id="${build}_${input_size}_c${c}_r${rep}_$(date +%s)"
        echo "== run: $run_id =="

        if [ "$simulate" = "1" ]; then
          # Generate a plausible simulated row (deterministic-ish)
          seed=$(( (c * rep) + ${#input_size} ))
          throughput=$((1000 + (seed % 500)))
          p50=$(awk -v s=$seed 'BEGIN{s=10 + (s%10); printf("%.1f", s)}')
          p95=$(awk -v s=$seed 'BEGIN{s=40 + (s%20); printf("%.1f", s)}')
          p99=$(awk -v s=$seed 'BEGIN{s=80 + (s%30); printf("%.1f", s)}')
          cpu=$(awk -v s=$seed 'BEGIN{s=20 + (s%50); printf("%.1f", s)}')
          rss=$((20000 + (seed * 100)))
          ts=$(timestamp)
          echo "${run_id},${build},${c},${input_size},${rep},${DURATION},${throughput},${p50},${p95},${p99},0.00,${cpu},${rss},simulated,${ts}" >> "$ALL_CSV"
          echo "SIMULATED -> $run_id"
          continue
        fi

        # Real run: start server
        SERVER_CMD=${SERVER_CMD:-$SERVER_CMD_DEFAULT}
        echo "Starting server: $SERVER_CMD"
        $SERVER_CMD &> "$LOG_DIR/server-${run_id}.log" &
        srv_pid=$!
        echo $srv_pid > "$PID_DIR/${run_id}.pid"

        # wait for it to be ready (simple sleep, consider healthcheck)
        sleep 1

        # Run wrk (requires wrk installed)
        echo "Running load: wrk -t2 -c${c} -d${DURATION}s ${ENDPOINT}"
        WRK_OUT=$(
          wrk -t2 -c${c} -d${DURATION}s ${ENDPOINT} 2>&1 || true
        )

        # Parse wrk output (best-effort)
        # Example: Requests/sec: 1250.00
        throughput=$(echo "$WRK_OUT" | awk -F: '/Requests\/sec/ {gsub(/ /,"",$2); print $2; exit}')
        p50=$(echo "$WRK_OUT" | awk '/Latency/ {print $2}' | sed 's/[,ms ]//g' | head -n1)
        # For p95/p99 we recommend scraping your app's /metrics or using more advanced tooling

        # Collect simple system stats
        read cpu rss <<< $(ps -p $srv_pid -o %cpu=,rss= | awk '{print $1, $2}') || true

        ts=$(timestamp)
        echo "${run_id},${build},${c},${input_size},${rep},${DURATION},${throughput:-0},${p50:-0},0,0,0.00,${cpu:-0},${rss:-0},ok,${ts}" >> "$ALL_CSV"

        echo "Stopping server pid $srv_pid"
        kill $srv_pid || true
        wait $srv_pid 2>/dev/null || true
      done
    done
  done
done

echo "All runs appended to $ALL_CSV"

echo "Done. To run in simulate mode: SIMULATE=1 ./perf/run_sweep.sh"
