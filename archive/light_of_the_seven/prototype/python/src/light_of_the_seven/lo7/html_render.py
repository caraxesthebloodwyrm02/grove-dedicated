from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

_BAR_SEC = 60.0 / 117.0


def render_heatmap_html(
    manifest: dict[str, Any],
    *,
    title: str = "Lo7 — document contribution heatmap",
    motion: bool = False,
) -> str:
    """Self-contained HTML; uses only manifest (no filesystem scan)."""
    h = manifest.get("heatmap") or {}
    cell_levels: list = h.get("cell_levels") or []
    cell_dates: list = h.get("cell_dates") or []
    days: dict = h.get("days") or {}
    days_json = json.dumps(days, ensure_ascii=False, sort_keys=True)
    motion_css = (
        f"""
    @keyframes lo7breathe {{ 0% {{ filter: brightness(0.9);}} 100% {{ filter: brightness(1.05);}} }}
    .lo7-motion .cell {{ animation: lo7breathe { _BAR_SEC:.3f }s ease-in-out infinite; }}
    """
        if motion
        else ""
    )

    rows_html: list[str] = []
    for wi, row in enumerate(cell_levels):
        cells = []
        for di, level in enumerate(row):
            iso = ""
            if wi < len(cell_dates) and di < len(cell_dates[wi]):
                iso = cell_dates[wi][di]
            day_hint = iso or f"W{wi + 1} D{di + 1}"
            level_cls = f"l{int(level)}"
            mid = f"lo7-grid-{wi}-{di}"
            cells.append(
                f'<td class="cell {level_cls}" data-iso="{html.escape(iso)}"'
                f' id="{html.escape(mid)}" title="{html.escape(day_hint)}"'
                f' data-level="{int(level)}" role="gridcell" tabindex="0"></td>'
            )
        rows_html.append(
            f'<tr><th class="wlab" scope="row">W{wi + 1:02d}</th>{"".join(cells)}</tr>'
        )

    th = '<tr><th class="corner" scope="col"></th>'
    dow = ("M", "T", "W", "T", "F", "S", "S")
    th += "".join(
        f'<th class="dow" scope="col">{html.escape(dow[i % 7])}</th>' for i in range(7)
    )
    th += "</tr>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #0d0f12;
      --fg: #c8d0dc;
      --l0: #1a1d23;
      --l1: #2e3a4a;
      --l2: #3d4f66;
      --l3: #4d6a8a;
      --l4: #6b8cbe;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; font-family: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif;
      background: var(--bg); color: var(--fg);
      min-height: 100vh; padding: 1.5rem;
    }}
    h1 {{ font-weight: 500; font-size: 1.1rem; letter-spacing: 0.02em; margin: 0 0 0.5rem; }}
    .sub {{ font-size: 0.8rem; opacity: 0.6; margin-bottom: 1rem; }}
    .grid-wrap {{ overflow: auto; max-width: 100%; }}
    table.grid {{
      border-collapse: separate; border-spacing: 3px; font-size: 0.7rem;
    }}
    .cell {{
      width: 10px; height: 10px; border-radius: 2px; cursor: pointer;
    }}
    .l0 {{ background: var(--l0);}}
    .l1 {{ background: var(--l1);}}
    .l2 {{ background: var(--l2);}}
    .l3 {{ background: var(--l3);}}
    .l4 {{ background: var(--l4);}}
    th.wlab {{ color: #5a6a7a; font-weight: 400; padding-right: 0.4rem; text-align: right; }}
    th.corner, th.dow {{ color: #4a5a6a; font-weight: 400; padding-bottom: 0.2rem; }}
    #panel {{
      margin-top: 1rem; padding: 0.8rem; background: #12151c; border-radius: 6px;
      min-height: 3rem; font-size: 0.85rem; line-height: 1.5; white-space: pre-wrap;
    }}
    {motion_css}
  </style>
</head>
<body class="{'lo7-motion' if motion else ''}">
  <h1>{html.escape(title)}</h1>
  <p class="sub">Indexed Silence — markdown by calendar day (local). No network; manifest-only.</p>
  <div class="grid-wrap">
  <table class="grid" role="grid" aria-label="52 week heatmap">
    {th}
    {''.join(rows_html)}
  </table>
  </div>
  <div id="panel" aria-live="polite">Click a cell for that day’s paths and titles.</div>
  <script>
    const days = {days_json};
    const panel = document.getElementById("panel");
    document.querySelectorAll("td.cell").forEach((td) => {{
      td.addEventListener("click", () => {{
        const iso = td.getAttribute("data-iso") || "";
        const lvl = td.getAttribute("data-level");
        const info = days[iso];
        const lines = [];
        lines.push(iso + " · level " + lvl);
        if (info && info.paths && info.paths.length) {{
          const ps = info.paths;
          const ts = info.titles || [];
          for (let i = 0; i < ps.length; i++) {{
            lines.push("• " + ps[i]);
            if (ts[i]) lines.push("  " + ts[i]);
          }}
        }} else {{
          lines.push("No documents in manifest for this day (empty or low weight).");
        }}
        panel.textContent = lines.join("\\n");
      }});
    }});
  </script>
</body>
</html>"""


def load_manifest_path(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
