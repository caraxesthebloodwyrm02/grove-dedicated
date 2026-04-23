# Lo7 quickstart (manifest + heatmap)

Prerequisites: repository root, `uv sync --group test` (or equivalent). Same commands as [README.md](../../README.md) and [docs/LO7_RUNBOOK.md](../../docs/LO7_RUNBOOK.md).

```bash
# From the light_of_the_seven repository root
mkdir -p _lo7
uv run lo7-manifest --config lo7_corpus.test.yaml --ref-date 2019-02-15 --out _lo7/manifest.json
uv run lo7-heatmap --in _lo7/manifest.json --out _lo7/heatmap.html
```

Open `_lo7/heatmap.html` in a browser. No network access is required; the heatmap is manifest-only.

**Parity (Python / Rust / Go):** build native services per the runbook, set `LO7_GO_BIN` if needed, then:

```bash
uv run --group test pytest tests/integration/test_lo7_manifest_parity.py -v --tb=short
```

Or: `make lo7-test` (see `tools/lo7_dev/lo7.mk`).
