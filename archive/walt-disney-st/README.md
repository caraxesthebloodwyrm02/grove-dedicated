# Python→Rust Contract Pipeline

A contract-first Python→JSON→Rust bridge that turns Python code into typed Rust data—with schema/type/build/run checks you can wire into CI.

## What is the Contract?

The contract is defined by two sources of truth:

1. **Python dataclasses** in [`artifact_generator.py`](artifact_generator.py):
   - `FunctionArtifact`
   - `ClassArtifact`
   - `ModuleArtifact`

2. **Rust structs** in [`rust/grid-core/src/lib.rs`](rust/grid-core/src/lib.rs):
   - Mirror the Python dataclasses with `serde` Serialize/Deserialize

3. **artifact.json** is the wire format:
   - Serialized from Python dataclasses
   - Deserialized by Rust structs
   - Contains `artifact_version` and `modules` array

The contract ensures that Python code introspection (AST parsing) produces artifacts that can be reliably consumed by Rust code, with validation at every stage.

## Quick Start

### Prerequisites

- Python 3.8+
- Rust toolchain (rustc, cargo)
- `jsonschema` Python package (optional, for JSON Schema validation)

```bash
pip install -r requirements.txt
```

### Running the Pipeline

The pipeline can be run via two entrypoints:

#### Shell Script (Recommended for CI)

```bash
./run_pipeline.sh
```

Environment variables:
- `ARTIFACT` - Path to artifact.json (default: `artifact.json`)
- `RUST_FILE` - Path to Rust structs file (default: `rust/grid-core/src/lib.rs`)
- `RUST_ROOT` - Rust workspace root (default: `rust`)
- `BIN` - Binary target to run (optional)
- `SKIP_RUN` - Set to `1` to skip runtime execution
- `MODE` - Validation mode: `artifact`, `cognitive`, or `both` (default: `artifact`)

#### Python Bridge

```bash
python application_bridge.py \
  --artifact artifact.json \
  --rust-file rust/grid-core/src/lib.rs \
  --root rust \
  --bin my-app \
  --skip-run
```

## Pipeline Stages

1. **Artifact Generation** (`artifact_generator.py`)
   - Parses Python AST
   - Generates `ModuleArtifact`, `ClassArtifact`, `FunctionArtifact`
   - Outputs JSON with `artifact_version` and `modules` array

2. **Schema Validation** (`schema_validator.py`)
   - Validates JSON structure
   - Supports `--engine handwritten|jsonschema|both`
   - Uses `schemas/artifact.schema.json` for JSON Schema validation

3. **Type Validation** (`type_validator.py`)
   - Compares Python dataclass fields vs Rust struct fields
   - Ensures field name parity (with `FIELD_NAME_MAPPING` support)
   - Parses Rust structs via regex from `--rust-file`

4. **Toolchain Validation** (`toolchain_validator.py`)
   - Checks `rustc` and `cargo` availability
   - Important for WSL vs Windows path issues

5. **Build Validation** (`build_validator.py`)
   - Runs `cargo build` in Rust workspace
   - Ensures code compiles

6. **Runtime Execution** (`runtime_executor.py`)
   - Runs `cargo run --bin <name>` (or default binary)
   - Passes `ARTIFACT_PATH` environment variable to Rust binary
   - Rust binary reads and processes `artifact.json`

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for detailed architecture diagrams.

## Value Proposition

- **Catch drift early**: Structural + type-shape validation before runtime
- **Reproducible**: Build/run is part of the contract pipeline
- **Extensible**: Add new contract models + validators
- **CI-ready**: Wire into GitHub Actions, GitLab CI, etc.

## Example: Rust Consumption

The `rust/my-app` binary demonstrates consuming `artifact.json`:

```bash
cd rust
cargo run --bin my-app -- --artifact ../artifact.json
```

Or with JSON output for CI:

```bash
cargo run --bin my-app -- --artifact ../artifact.json --json
```

The binary generates reports on:
- Total modules, functions, classes, methods
- Docstring coverage statistics
- Import graph summary
- Class/method counts

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines on:
- Adding new contract models
- Adding new validators
- Good first issues
- Development setup

## License

[Add your license here]

