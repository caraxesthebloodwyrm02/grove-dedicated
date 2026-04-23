#!/usr/bin/env bash
set -euo pipefail

# Thin wrapper around application_bridge.py for CI compatibility
# All orchestration logic is now in application_bridge.py

ARTIFACT="${ARTIFACT:-artifact.json}"
RUST_FILE="${RUST_FILE:-rust/grid-core/src/lib.rs}"
RUST_ROOT="${RUST_ROOT:-rust}"
BIN="${BIN:-}"
SKIP_RUN="${SKIP_RUN:-0}"
MODE="${MODE:-artifact}"
SCHEMA_ENGINE="${SCHEMA_ENGINE:-handwritten}"

# Build command arguments
CMD_ARGS=(
  "--artifact" "${ARTIFACT}"
  "--rust-file" "${RUST_FILE}"
  "--root" "."
  "--schema-engine" "${SCHEMA_ENGINE}"
  "--mode" "${MODE}"
)

if [[ -n "${BIN}" ]]; then
  CMD_ARGS+=("--bin" "${BIN}")
fi

if [[ "${SKIP_RUN}" == "1" ]]; then
  CMD_ARGS+=("--skip-run")
fi

# Run the canonical pipeline runner
python application_bridge.py "${CMD_ARGS[@]}"
