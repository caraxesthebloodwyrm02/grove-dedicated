"""
Interactive visualization of the Circle of Fifths using Plotly.

This script generates an interactive circular graph where:
- Nodes represent keys (e.g., C, G, D).
- Edges represent intervals (e.g., perfect fifths).
- Hover effects provide additional information.

Can be run standalone or imported as a module.

Part of the GRID project: E:\\GRID\\light_of_the_seven\\full_datakit
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

# Path configuration for GRID integration
SCRIPT_DIR = Path(__file__).parent
VISUALIZATIONS_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = VISUALIZATIONS_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"

# Default Circle of Fifths keys (fallback)
DEFAULT_KEYS = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F"]

# Lazy imports to avoid circular dependencies
if TYPE_CHECKING:
    import networkx as nx
    import plotly.graph_objects as go


def _get_networkx():
    """Lazy import for networkx to avoid circular imports."""
    try:
        import networkx as nx

        return nx
    except ImportError:
        print("Error: networkx is required. Install with: pip install networkx")
        sys.exit(1)


def _get_plotly():
    """Lazy import for plotly to avoid circular imports."""
    try:
        import plotly.graph_objects as go

        return go
    except ImportError:
        print("Error: plotly is required. Install with: pip install plotly")
        sys.exit(1)


def load_circle_data() -> Dict[str, Any]:
    """
    Load full Circle of Fifths data from JSON.

    Returns:
        Dictionary with circle data, or minimal defaults if file not found.
    """
    json_path = DATA_DIR / "circle_of_fifths.json"
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✅ Loaded data from: {json_path}")
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"⚠️  Could not load JSON: {e}")
        print("   Using default keys.")
        return {"keys": DEFAULT_KEYS}


def load_keys_from_json() -> List[str]:
    """
    Load just the keys from the circle_of_fifths.json data file.

    Returns:
        List of musical keys, or defaults if file not found.
    """
    data = load_circle_data()
    return data.get("keys", DEFAULT_KEYS)


def create_circle_of_fifths_graph(
    keys: Optional[List[str]] = None,
) -> Tuple[Any, List[str]]:
    """
    Create a graph of the Circle of Fifths.

    Args:
        keys: List of musical keys. If None, loads from JSON or uses defaults.

    Returns:
        Tuple of (NetworkX Graph, list of keys)
    """
    nx = _get_networkx()

    if keys is None:
        keys = load_keys_from_json()

    # Create a graph
    G = nx.Graph()

    # Add nodes (keys)
    G.add_nodes_from(keys)

    # Add edges (perfect fifths - adjacent keys in the circle)
    for i in range(len(keys)):
        G.add_edge(keys[i], keys[(i + 1) % len(keys)])

    return G, keys


def draw_interactive_circle_graph(
    G: Any,
    keys: List[str],
    output_path: Optional[Path] = None,
    show: bool = True,
    title: str = "Interactive Circle of Fifths",
    node_color: str = "lightblue",
    edge_color: str = "gray",
    width: int = 800,
    height: int = 800,
    extra_data: Optional[Dict[str, Any]] = None,
) -> Path:
    """
    Draw the Circle of Fifths as an interactive Plotly graph.

    Args:
        G: NetworkX graph object
        keys: List of keys for labeling
        output_path: Path to save the HTML file. If None, saves to project root.
        show: Whether to open the plot in browser
        title: Title for the graph
        node_color: Color for nodes
        edge_color: Color for edges
        width: Figure width in pixels
        height: Figure height in pixels
        extra_data: Additional data dict for enhanced hover info

    Returns:
        Path to the saved HTML file.
    """
    nx = _get_networkx()
    go = _get_plotly()

    # Define the layout (circular)
    pos = nx.circular_layout(G)

    # Extract node positions
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    # Extract edge positions
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Create hover text with extra info if available
    hover_texts = []
    for key in keys:
        hover = f"<b>Key: {key}</b>"
        if extra_data:
            # Add key signature info
            signatures = extra_data.get("key_signatures", {})
            if key in signatures:
                sig = signatures[key]
                sharps = sig.get("sharps", 0)
                flats = sig.get("flats", 0)
                if sharps > 0:
                    hover += f"<br>Sharps: {sharps}"
                elif flats > 0:
                    hover += f"<br>Flats: {flats}"
                else:
                    hover += "<br>No sharps or flats"

            # Add relative minor
            rel_minors = extra_data.get("relative_minors", {})
            if key in rel_minors:
                hover += f"<br>Relative minor: {rel_minors[key]}"

            # Add relationships
            relationships = extra_data.get("relationships", {})
            if key in relationships:
                neighbors = relationships[key]
                if len(neighbors) >= 2:
                    hover += f"<br>→ Fifth: {neighbors[0]}"
                    hover += f"<br>→ Fourth: {neighbors[1]}"

        hover_texts.append(hover)

    # Create the figure
    fig = go.Figure()

    # Add edges
    fig.add_trace(
        go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(width=2, color=edge_color),
            hoverinfo="none",
            name="Perfect Fifths",
        )
    )

    # Add nodes
    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=keys,
            textposition="top center",
            textfont=dict(size=14, color="black"),
            marker=dict(
                size=40,
                color=node_color,
                line=dict(width=2, color="darkblue"),
            ),
            hoverinfo="text",
            hovertext=hover_texts,
            name="Keys",
        )
    )

    # Update layout
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20),
            x=0.5,
            xanchor="center",
        ),
        showlegend=False,
        width=width,
        height=height,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-1.5, 1.5],
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-1.5, 1.5],
        ),
        plot_bgcolor="white",
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Arial",
        ),
        annotations=[
            dict(
                text="Click and drag to pan. Scroll to zoom. Hover for details.",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=-0.05,
                font=dict(size=12, color="gray"),
            )
        ],
    )

    # Determine output path
    if output_path is None:
        output_path = PROJECT_ROOT / "interactive_circle.html"
    else:
        output_path = Path(output_path)

    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the HTML
    fig.write_html(str(output_path), include_plotlyjs=True, full_html=True)
    print(f"✅ Interactive visualization saved to: {output_path}")

    # Show if requested
    if show:
        fig.show()

    return output_path


def main() -> None:
    """Main entry point for standalone execution."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate an interactive Circle of Fifths visualization with Plotly"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output HTML file path (default: project_root/interactive_circle.html)",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Don't open the visualization in browser",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="Interactive Circle of Fifths",
        help="Title for the visualization",
    )
    parser.add_argument(
        "--node-color",
        type=str,
        default="lightblue",
        help="Color for nodes (default: lightblue)",
    )
    parser.add_argument(
        "--edge-color",
        type=str,
        default="gray",
        help="Color for edges (default: gray)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=800,
        help="Figure width in pixels (default: 800)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=800,
        help="Figure height in pixels (default: 800)",
    )

    args = parser.parse_args()

    print("🎵 Circle of Fifths - Interactive Plotly Visualization")
    print("-" * 55)
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Data directory: {DATA_DIR}")
    print("-" * 55)

    # Load full data for enhanced hover info
    circle_data = load_circle_data()
    keys = circle_data.get("keys", DEFAULT_KEYS)

    # Create the graph
    G, keys = create_circle_of_fifths_graph(keys)
    print(f"Loaded {len(keys)} keys: {', '.join(keys[:6])}...")

    # Draw and save
    output_path = Path(args.output) if args.output else None
    draw_interactive_circle_graph(
        G,
        keys,
        output_path=output_path,
        show=not args.no_show,
        title=args.title,
        node_color=args.node_color,
        edge_color=args.edge_color,
        width=args.width,
        height=args.height,
        extra_data=circle_data,
    )

    print("\n💡 Tip: Open the HTML file in a browser for full interactivity!")


if __name__ == "__main__":
    main()
