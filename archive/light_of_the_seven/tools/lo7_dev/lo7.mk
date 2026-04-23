# Lo7 dev package — include from repo root Makefile (see tools/lo7_dev/README.md)
# Run `make` from the repository root so REPO_ROOT resolves correctly.

REPO_ROOT ?= $(CURDIR)
LO7_DEV_DIR := $(REPO_ROOT)/tools/lo7_dev

# Reference corpus (override on CLI): make lo7-bench REF_CONFIG=lo7_corpus.yaml REF_DATE=2019-06-01
REF_CONFIG ?= lo7_corpus.test.yaml
REF_DATE ?= 2019-02-15

GO_RELEASE := /tmp/lo7-go-release
GO_DEBUG := /tmp/lo7-go

# Bare `make` — same as `make help`
.DEFAULT_GOAL := help

SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

# Shell scripts to chmod +x (dev + Lo7 scaffolds)
EXEC_SCRIPTS := \
	$(REPO_ROOT)/scripts/lo7_generate.sh \
	$(REPO_ROOT)/scripts/lo7_benchmark.sh \
	$(REPO_ROOT)/scripts/install-hooks.sh \
	$(REPO_ROOT)/setup_venv.sh

.PHONY: help package executable chmod-scripts refs lo7-refs \
	lo7-release lo7-bench lo7-test

help:
	@echo "Lo7 dev package (tools/lo7_dev) — run from repo root: cd \$$(REPO_ROOT) && make <target>"
	@echo ""
	@echo "  make package   — list this package + reference prototypes"
	@echo "  make executable — chmod +x on EXEC_SCRIPTS (see Makefile)"
	@echo "  make refs     — print REF_CONFIG / REF_DATE and prototype paths"
	@echo "  make lo7-release  — release Rust + Go (Go -> $(GO_RELEASE))"
	@echo "  make lo7-bench  — bench using REF_CONFIG=$(REF_CONFIG) REF_DATE=$(REF_DATE)"
	@echo "  make lo7-test   — integration parity (Python / Rust / Go)"
	@echo ""
	@echo "Overrides:  make lo7-bench REF_CONFIG=lo7_corpus.yaml REF_DATE=2020-01-15"

# Batch metadata: this folder + what it points at
package: refs
	@echo ""
	@echo "Package dir: $(LO7_DEV_DIR)"
	@ls -la "$(LO7_DEV_DIR)" 2>/dev/null || true

refs lo7-refs:
	@echo "Lo7 reference bundle (prototypes we scaffolded):"
	@echo "  REF_CONFIG     = $(REF_CONFIG)  (override: make lo7-bench REF_CONFIG=lo7_corpus.yaml)"
	@echo "  REF_DATE       = $(REF_DATE)    (for heatmap window end / bench)"
	@echo "  test corpus:    $(REPO_ROOT)/lo7_corpus.test.yaml  +  $(REPO_ROOT)/tools/octopus_fixtures/mini_docs/"
	@echo "  prod corpus:   $(REPO_ROOT)/lo7_corpus.yaml"
	@echo "  schema:         $(REPO_ROOT)/tools/octopus/lo7_manifest_v1.schema.json"
	@echo "  runbook:        $(REPO_ROOT)/docs/LO7_RUNBOOK.md"
	@echo "  parity test:   $(REPO_ROOT)/tests/integration/test_lo7_manifest_parity.py"
	@echo "  rust service:  $(REPO_ROOT)/prototype/rust/lo7-manifest-service/"
	@echo "  go service:     $(REPO_ROOT)/prototype/go/lo7_manifest_service/"
	@echo "  python lo7:      $(REPO_ROOT)/prototype/python/src/light_of_the_seven/lo7/  (symlink: src/.../lo7)"
	@echo "  notebook proto:  $(REPO_ROOT)/notebooks/lo7_emergent_matrix.ipynb  +  $(REPO_ROOT)/docs/LO7_NOTEBOOK_PROTOTYPE.md"

# Make scaffolds runnable
executable chmod-scripts:
	@chmod -v +x $(EXEC_SCRIPTS)

lo7-release: executable
	cd "$(REPO_ROOT)/prototype/rust" && cargo build --release -p lo7-manifest-service
	cd "$(REPO_ROOT)/prototype/go/lo7_manifest_service" && go build -ldflags="-s -w" -o "$(GO_RELEASE)" .

lo7-bench: executable
	@test -x "$(REPO_ROOT)/scripts/lo7_benchmark.sh" || { echo "Run: make executable"; exit 1; }
	cd "$(REPO_ROOT)" && LO7_BENCH_PRECISE=1 LO7_BENCH_RUNS=5 \
		./scripts/lo7_benchmark.sh "$(REF_CONFIG)" "$(REF_DATE)"

lo7-test: executable
	@test -d "$(REPO_ROOT)/.venv" || { echo "Run: uv sync --group test"; exit 1; }
	cd "$(REPO_ROOT)/prototype/rust" && cargo build -p lo7-manifest-service
	cd "$(REPO_ROOT)/prototype/go/lo7_manifest_service" && go build -o "$(GO_DEBUG)" .
	cd "$(REPO_ROOT)" && LO7_GO_BIN="$(GO_DEBUG)" uv run --group test \
		pytest tests/integration/test_lo7_manifest_parity.py -v
