import argparse

from src.embeddings import create_query_embedding
from src.database import search_similar_chunks


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Perform semantic search over indexed documents."
    )

    parser.add_argument(
        "--query",
        required=True,
        help="Search query."
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Maximum number of results to return."
    )

    parser.add_argument(
    "--strategy",
    choices=["fixed", "sentence", "paragraph"],
    help="Optional chunking strategy filter."
    )   

    return parser.parse_args()


def search(query: str, limit: int, strategy: str | None):
    """
    Generate a query embedding and retrieve similar chunks.
    """

    print(f'Searching for: "{query}"')

    query_embedding = create_query_embedding(query)

    results = search_similar_chunks(
    query_embedding=query_embedding,
    limit=limit,
    strategy=strategy
    )

    if not results:
        print("No matching results found.")
        return

    print()
    print(f"Top {len(results)} results:")
    print("=" * 70)

    for index, result in enumerate(results, start=1):
        chunk_id, chunk_text, filename, split_strategy, similarity = result

        print(f"\nResult {index}")
        print(f"Similarity: {similarity:.4f}")
        print(f"File: {filename}")
        print(f"Strategy: {split_strategy}")
        print("Text:")
        print(chunk_text)
        print("-" * 70)


def main():
    args = parse_arguments()

    try:
        search(
            query=args.query,
            limit=args.limit,
            strategy=args.strategy
        )

    except ValueError as error:
        print(f"Input error: {error}")

    except ConnectionError as error:
        print(f"Database connection error: {error}")

    except RuntimeError as error:
        print(f"Search error: {error}")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()