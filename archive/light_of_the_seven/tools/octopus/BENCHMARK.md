# Lo7 manifest service — benchmark and default selection (step 7)

**Rule:** this file must exist *before* the first “real” benchmark run (step 9).  
Step **9** may only include implementations that **passed** step **8** (integration).  
Step **10** applies *only* the text in *this* file to choose a default binary.

## Metrics (suggested)

- Cold start: one manifest generation after process spawn (stdio in CI).
- Warm: second run in the same process (if supported).
- Serialize: time to `json` encode the manifest object.
- N requests: batch of N identical corpus reads (optional).

## Default selection (step 10)

1. All candidates must be **identical** normalized JSON to the step **8** golden for `lo7_corpus.test.yaml` + `tools/octopus_fixtures/mini_docs/`.
2. Among passers, prefer **lowest p95** cold time on the reference machine, then **smallest** binary size, then order: Python, Rust, Go (tie-break).
3. Set `LO7_DEFAULT_MANIFEST_SERVICE` in CI / runbook to the chosen executable path or label.

**Normalization:** `json.dumps(obj, sort_keys=True)` (Python) or byte-identical minified order from each language’s canonical serializer. For parity tests, use sorted keys and stable array order.

## Level thresholds (must match all implementations)


| Files contributing to a calendar day (weight = count) | Level                                 |
| ----------------------------------------------------- | ------------------------------------- |
| 0                                                     | 0 (or `empty_cell_level` from config) |
| 1                                                     | 1                                     |
| 2                                                     | 2                                     |
| 3–4                                                   | 3                                     |
| 5+                                                    | 4                                     |


This table is part of the contract; do not “tune” per language.