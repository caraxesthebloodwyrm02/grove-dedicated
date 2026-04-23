# perf — Spectrum Sweep Runner

This folder contains simple runner scripts to perform a spectrum sweep (build modes × concurrency × input size) against the `magical_forest` binary.

Files
- `run_sweep.sh` — Bash runner for WSL/Linux/macOS. Supports `SIMULATE=1` which emits simulated CSV rows and does not execute builds or network load.
- `run_sweep.ps1` — Powershell runner with `-Simulate` switch for Windows.
- `results/all_runs.csv` — CSV file where runs are appended. The script creates it and writes a header if missing.

Quickstart (simulate)

Bash (WSL):

```bash
cd <repo-root>
SIMULATE=1 ./perf/run_sweep.sh
```

PowerShell (Windows):

```powershell
.\perf\run_sweep.ps1 -Simulate
```

Real runs
- Requirements: `cargo`, `wrk` (or change `run_sweep.sh` to use a different load generator), and a compiled release binary (`cargo build --release`).
- The scripts assume the server is available at `http://127.0.0.1:8080/`. Change `ENDPOINT` in the scripts to match your app.

Notes
- LTO build uses `RUSTFLAGS="-C lto -C codegen-units=1"` during build.
- The scripts do basic parsing of `wrk` output. For robust latency percentiles and engagement metrics, instrument your app (see next steps in the project TODOs).

Next steps
- Implement feature-gated instrumentation behind a Cargo feature `perf` to export histograms and counters.
- Add a CI workflow to run a small simulated matrix and upload the CSV as an artifact.
