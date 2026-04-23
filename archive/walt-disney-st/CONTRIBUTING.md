# Contributing Guide

Thank you for your interest in contributing to the Python→Rust Contract Pipeline! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.8+
- Rust toolchain (rustc, cargo)
- Git

### Setup Steps

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Verify Rust toolchain:
   ```bash
   rustc --version
   cargo --version
   ```
4. Run the pipeline to verify setup:
   ```bash
   ./run_pipeline.sh
   ```

## Adding a New Contract Model

Contract models are defined in two places that must stay in sync:

1. **Python dataclass** in [`artifact_generator.py`](artifact_generator.py)
2. **Rust struct** in [`rust/grid-core/src/lib.rs`](rust/grid-core/src/lib.rs)

### Steps

1. Add Python dataclass:
   ```python
   @dataclass
   class YourArtifact:
       name: str
       value: int
   ```

2. Add corresponding Rust struct:
   ```rust
   #[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
   pub struct YourArtifact {
       pub name: String,
       pub value: usize,
   }
   ```

3. Update `type_validator.py` to include your new model in `load_python_contracts()`

4. Update `schemas/artifact.schema.json` to include your new artifact type

5. Run validation:
   ```bash
   python type_validator.py --rust-file rust/grid-core/src/lib.rs
   ```

## Adding a New Validator

Validators ensure the contract remains valid. You can add custom validators in two ways:

### Method 1: Standalone Validator Script

Create a new Python script (e.g., `your_validator.py`):

```python
from pathlib import Path
import sys

def validate(artifact_path: Path) -> list[str]:
    """Return list of error messages, or empty list if valid."""
    errors = []
    # Your validation logic here
    return errors

if __name__ == "__main__":
    artifact = Path(sys.argv[1])
    errors = validate(artifact)
    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
    print("Validation passed.")
```

Then add it to the pipeline in `application_bridge.py` or `run_pipeline.sh`.

### Method 2: Validator Registry (Future)

The validator registry allows registering validators dynamically. See [`examples/custom_validator.py`](examples/custom_validator.py) for an example.

## Good First Issues

These are great starting points for new contributors:

### Easy

1. **Add docstring coverage report to my-app**
   - Enhance `rust/my-app/src/main.rs` to show which modules/functions/classes are missing docstrings
   - Output as markdown or JSON

2. **Add JSON Schema validator option**
   - Already implemented! But you can enhance it with better error messages or additional validation rules

3. **Windows/WSL robustness improvements**
   - Test and improve path handling in validators
   - Add better error messages for common Windows/WSL issues

### Medium

4. **CI workflow for run_pipeline.sh on PRs**
   - Already implemented! But you can enhance it with:
     - Status check summary comments
     - Artifact comparison between PR and main branch
     - Performance benchmarks

5. **Add a proper JSON Schema file**
   - Already created! But you can enhance it with:
     - More detailed constraints
     - Custom validation rules
     - Better error messages

### Advanced

6. **Cognitive contracts mode expansion**
   - Expand `--mode cognitive` support in `type_validator.py`
   - Add validation for cognitive model contracts

7. **Groundedness-style evidence reports**
   - Create reports that attach artifacts + provenance
   - Link validation results to specific commits/PRs

## Code Style

### Python

- Use type hints
- Follow PEP 8
- Use `black` for formatting (if configured)
- Add docstrings for public functions

### Rust

- Follow `rustfmt` defaults
- Use `clippy` for linting
- Add doc comments for public items

## Testing

Before submitting a PR:

1. Run the full pipeline:
   ```bash
   ./run_pipeline.sh
   ```

2. Test your changes:
   ```bash
   python schema_validator.py artifact.json --engine both
   python type_validator.py --rust-file rust/grid-core/src/lib.rs
   ```

3. Verify Rust code compiles:
   ```bash
   cd rust
   cargo build
   cargo test
   ```

4. Test Rust binary:
   ```bash
   cd rust
   cargo run --bin my-app -- --artifact ../artifact.json
   ```

## Submitting Changes

1. Create a feature branch from `main`
2. Make your changes
3. Run the validation pipeline
4. Commit with clear messages
5. Push and create a pull request
6. Ensure CI passes

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for design questions
- Check existing issues/PRs for similar work

Thank you for contributing!

