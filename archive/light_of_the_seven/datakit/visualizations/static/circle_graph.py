"""
Static visualization of the Circle of Fifths using matplotlib.

This script generates a circular graph where:
- Nodes represent keys (e.g., C, G, D).
- Edges represent intervals (e.g., perfect fifths).

Can be run standalone or imported as a module.

Part of the GRID project: E:\\GRID\\light_of_the_seven\\full_datakit
"""

import json
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# Path configuration for GRID integration
SCRIPT_DIR = Path(__file__).parent
VISUALIZATIONS_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = VISUALIZATIONS_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"

# Add project root to path for imports
sys.path.insert(0, str(PROJECT_ROOT))

# Default Circle of Fifths keys (fallback)
DEFAULT_KEYS = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F"]


def load_keys_from_json() -> List[str]:
    """
    Load keys from the circle_of_fifths.json data file.

    Returns:
        List of musical keys, or defaults if file not found.
    """
    json_path = DATA_DIR / "circle_of_fifths.json"
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("keys", DEFAULT_KEYS)
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_KEYS


def create_circle_of_fifths_graph(keys: Optional[List[str]] = None):
    """
    Create a graph of the Circle of Fifths.

    Args:
        keys: List of musical keys. If None, loads from JSON or uses defaults.

    Returns:
        Tuple of (NetworkX Graph, list of keys)
    """
    try:
        import networkx as nx
    except ImportError:
        print("Error: networkx is required. Install with: pip install networkx")
        sys.exit(1)

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


def draw_circle_graph(
    G,
    keys: List[str],
    output_path: Optional[Path] = None,
    show: bool = True,
    title: str = "Circle of Fifths",
    node_color: str = "lightblue",
    edge_color: str = "gray",
    figsize: Tuple[int, int] = (10, 10),
):
    """
    Draw the Circle of Fifths as a circular graph.

    Args:
        G: NetworkX graph object
        keys: List of keys for labeling
        output_path: Path to save the image. If None, saves to project root.
        show: Whether to display the plot interactively
        title: Title for the graph
        node_color: Color for nodes
        edge_color: Color for edges
        figsize: Figure size as (width, height)
    """
    try:
        import matplotlib.pyplot as plt
        import networkx as nx
    except ImportError as e:
        print(
            f"Error: Missing dependency. Install with: pip install matplotlib networkx"
        )
        print(f"Details: {e}")
        sys.exit(1)

    # Set up the figure
    plt.figure(figsize=figsize)

    # Define the layout (circular)
    pos = nx.circular_layout(G)

    # Draw nodes and edges
    nx.draw_networkx_nodes(G, pos, node_color=node_color, node_size=1000)
    nx.draw_networkx_edges(G, pos, edge_color=edge_color, width=1)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

    # Add title and remove axes
    plt.title(title, fontsize=16)
    plt.axis("off")

    # Determine output path
    if output_path is None:
        output_path = PROJECT_ROOT / "circle_graph.png"
    else:
        output_path = Path(output_path)

    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the graph
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"✅ Static visualization saved to: {output_path}")

    # Show if requested
    if show:
        plt.show()
    else:
        plt.close()

    return output_path


def main():
    """Main entry point for standalone execution."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a static Circle of Fifths visualization"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output file path (default: project_root/circle_graph.png)",
    )
    parser.add_argument(
        "--no-show", action="store_true", help="Don't display the plot interactively"
    )
    parser.add_argument(
        "--title",
        type=str,
        default="Circle of Fifths",
        help="Title for the visualization",
    )
    parser.add_argument(
        "--node-color",
        type=str,
        default="lightblue",
        help="Color for nodes (default: lightblue)",
    )
    parser.add_argument(
        "--edge-color", type=str, default="gray", help="Color for edges (default: gray)"
    )

    args = parser.parse_args()

    print("🎵 Circle of Fifths - Static Visualization Generator")
    print("-" * 50)
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Data directory: {DATA_DIR}")
    print("-" * 50)

    # Create the graph
    G, keys = create_circle_of_fifths_graph()
    print(f"Loaded {len(keys)} keys: {', '.join(keys[:6])}...")

    # Draw and save
    output_path = Path(args.output) if args.output else None
    draw_circle_graph(
        G,
        keys,
        output_path=output_path,
        show=not args.no_show,
        title=args.title,
        node_color=args.node_color,
        edge_color=args.edge_color,
    )


if __name__ == "__main__":
    main()
