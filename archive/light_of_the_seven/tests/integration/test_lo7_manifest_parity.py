"""
Step 8(b): same manifest (normalized) across Python, Rust, and Go for the test corpus.
Mtimes on fixture files are fixed so day buckets are deterministic.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
CONFIG = REPO / "lo7_corpus.test.yaml"
MINI = REPO / "tools" / "octopus_fixtures" / "mini_docs"
PY = REPO / ".venv" / "bin" / "lo7-manifest"
RS = REPO / "prototype" / "rust" / "target" / "debug" / "lo7-manifest-service"
GO_BUILD = REPO / "prototype" / "go" / "lo7_manifest_service"
REF_DATE = "2019-02-15"


@pytest.fixture
def _fixed_mtimes() -> None:
    import datetime

    t0 = datetime.datetime(2019, 1, 1, 12, 0, 0).timestamp()
    t1 = datetime.datetime(2019, 1, 2, 12, 0, 0).timestamp()
    os.utime(MINI / "alpha.md", (t0, t0))
    os.utime(MINI / "beta.md", (t1, t1))


def _run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, check=False, capture_output=True, text=True, cwd=REPO)
    assert r.returncode == 0, r.stderr + r.stdout


def _load(p: Path) -> dict:
    with p.open(encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.usefixtures("_fixed_mtimes")
def test_python_manifest_regression() -> None:
    if not PY.exists():
        pytest.skip("no venv lo7-manifest")
    out = REPO / "_lo7" / "pytest_manifest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    _run([str(PY), "--config", str(CONFIG), "--ref-date", REF_DATE, "--out", str(out)])
    m = _load(out)
    assert m["schema_version"] == "1"
    assert m["type_name"] == "OctopusManifest"
    assert m["body"]["file_count"] >= 2
    assert "heatmap" in m
    assert len(m["heatmap"]["cell_levels"]) == 52


@pytest.mark.usefixtures("_fixed_mtimes")
def test_three_language_parity() -> None:
    if not (PY.exists() and RS.exists()):
        pytest.skip(
            "build Python venv and: cd prototype/rust && cargo build -p lo7-manifest-service"
        )
    go_bin = os.environ.get("LO7_GO_BIN", "/tmp/lo7-go")
    if not Path(go_bin).exists():
        pytest.skip("run: cd prototype/go/lo7_manifest_service && go build -o /tmp/lo7-go .")
    py_out = REPO / "_lo7" / "parity_py.json"
    rs_out = REPO / "_lo7" / "parity_rs.json"
    go_out = REPO / "_lo7" / "parity_go.json"
    for p in (py_out, rs_out, go_out):
        p.parent.mkdir(parents=True, exist_ok=True)
    _run([str(PY), "--config", str(CONFIG), "--ref-date", REF_DATE, "--out", str(py_out)])
    _run([str(RS), "--config", str(CONFIG), "--ref-date", REF_DATE, "--out", str(rs_out)])
    _run([go_bin, "--config", str(CONFIG), "--ref-date", REF_DATE, "--out", str(go_out)])
    a, b, c = _load(py_out), _load(rs_out), _load(go_out)
    assert a == b
    assert b == c


def test_heatmap_renders_from_manifest_only() -> None:
    from light_of_the_seven.lo7.build import build_manifest, manifest_to_canonical_json
    from light_of_the_seven.lo7.config import load_corpus_config
    from light_of_the_seven.lo7.html_render import load_manifest_path, render_heatmap_html

    cfg = load_corpus_config(CONFIG)
    m = build_manifest(cfg)
    s = manifest_to_canonical_json(m)
    p = REPO / "_lo7" / "inline.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")
    html = render_heatmap_html(load_manifest_path(p))
    assert "grid" in html
    assert "Indexed Silence" in html
    assert "days" in html
    # Well-formed document shell (E2E HTML contract; no browser required)
    low = html.lower()
    assert low.lstrip().startswith("<!doctype html")
    assert "<html" in low and "</html>" in html
    assert 'charset="utf-8"' in low
    assert 'role="grid"' in html
    assert len(html) >= 2500, "heatmap HTML unexpectedly small; possible empty render"
