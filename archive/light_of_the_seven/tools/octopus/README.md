# Octopus (Lo7) — tools

- [`lo7_manifest_v1.schema.json`](lo7_manifest_v1.schema.json) — JSON Schema for the Lo7 document manifest (v1). Code name: **OctopusManifest** (document in source if kept).
- [`BENCHMARK.md`](BENCHMARK.md) — benchmark rules; must exist before first official benchmark (§5 step 7).

## §2.1 defaults (operator + implementer)

- **Root:** default repo root = arch_data `light_of_the_seven` (see repository `lo7_corpus.yaml`); not `~/gruff/workspace`.
- **Day bucket:** local wall calendar day; if CI uses UTC, document and test.
- **Per-file day:** mtime, optional YAML frontmatter `date: YYYY-MM-DD` override.
- **Title:** first H1, else file stem.
- **Renderer:** may read only the manifest (or a snapshot) — no repository walk.
- **Default service env:** set `LO7_DEFAULT_MANIFEST_SERVICE` only after successful steps 8, 9, 10 (see BENCHMARK.md). **Recorded choice (2026-04-24, Prince):** Go release binary at `/tmp/lo7-go-release` — `export LO7_DEFAULT_MANIFEST_SERVICE="/tmp/lo7-go-release"` (rebuild with `make lo7-release`). Prefer a fixed install path in production.

## Commands (after `uv sync`)

```bash
# Manifest JSON (stdio or file)
uv run lo7-manifest --config lo7_corpus.test.yaml --out - | jq .

# Static heatmap HTML from manifest (no repo walk)
uv run lo7-heatmap --in manifest.json --out _lo7/heatmap.html
```

## Cross-language services

- Python: `lo7-manifest` (this package)
- Rust: `prototype/rust/lo7-manifest-service/`
- Go: `prototype/go/lo7_manifest_service/`

Parity is enforced by `tests/integration/test_lo7_manifest_parity.py`.
