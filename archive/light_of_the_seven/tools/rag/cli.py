#!/usr/bin/env python3
"""
RAG CLI interface for GRID.

Provides command-line interface for indexing repositories and querying
the RAG system using the unified RAG engine.
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add the grid root to Python path
grid_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(grid_root))

from tools.rag.config import RAGConfig  # noqa: E402
from tools.rag.rag_engine import RAGEngine  # noqa: E402


def setup_parser():
    """Setup argument parser for RAG CLI."""
    parser = argparse.ArgumentParser(
        description="RAG (Retrieval-Augmented Generation) CLI for GRID"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Index command
    index_parser = subparsers.add_parser("index", help="Index a repository")
    index_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to repository to index (default: current directory)",
    )
    index_parser.add_argument(
        "--rebuild", action="store_true", help="Rebuild index even if it exists"
    )

    # Query command
    query_parser = subparsers.add_parser("query", help="Query the RAG system")
    query_parser.add_argument("query", help="Query string")
    query_parser.add_argument(
        "--top-k", type=int, default=5, help="Number of results to retrieve (default: 5)"
    )
    query_parser.add_argument(
        "--temperature", type=float, default=0.7, help="LLM temperature (default: 0.7)"
    )

    # Stats command
    subparsers.add_parser("stats", help="Show RAG system statistics")

    return parser


async def index_command(args):
    """Handle index command."""
    print(f"Indexing repository at: {args.path}")

    try:
        config = RAGConfig.from_env()
        config.ensure_local_only()

        engine = RAGEngine(config=config)
        engine.index(repo_path=args.path, rebuild=args.rebuild)

        print("Indexing completed successfully!")
        stats = engine.get_stats()
        print(f"Total documents indexed: {stats['document_count']}")

    except Exception as e:
        print(f"Error indexing repository: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


async def query_command(args):
    """Handle query command."""
    print(f"Querying: {args.query}")

    try:
        config = RAGConfig.from_env()
        config.ensure_local_only()

        engine = RAGEngine(config=config)
        result = engine.query(query_text=args.query, top_k=args.top_k, temperature=args.temperature)

        print("\nAnswer:")
        print(result["answer"])

        if result.get("sources"):
            print(f"\nSources ({len(result['sources'])}):")
            for i, source in enumerate(result["sources"], 1):
                print(
                    f"  {i}. {source['metadata'].get('path', 'Unknown')} "
                    f"(distance: {source['distance']:.3f})"
                )

    except Exception as e:
        print(f"Error querying RAG system: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


async def stats_command(args):
    """Handle stats command."""
    try:
        config = RAGConfig.from_env()
        engine = RAGEngine(config=config)
        stats = engine.get_stats()

        print("RAG System Statistics:")
        print(f"  Documents: {stats['document_count']}")
        print(f"  Collection: {stats['collection_name']}")
        print(f"  Embedding Model: {stats['embedding_model']}")
        print(f"  LLM Model: {stats['llm_model']}")

    except Exception as e:
        print(f"Error getting stats: {e}")
        return 1

    return 0


async def main():
    """Main CLI entry point."""
    parser = setup_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "index":
        return await index_command(args)
    elif args.command == "query":
        return await query_command(args)
    elif args.command == "stats":
        return await stats_command(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
