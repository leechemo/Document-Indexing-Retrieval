import argparse
from pathlib import Path

from src.document_loader import load_document
from src.chunker import chunk_text
from src.embeddings import create_embedding
from src.database import initialize_database, insert_chunk


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Index a PDF or DOCX document into PostgreSQL using Gemini embeddings."
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Path to the PDF or DOCX file."
    )

    parser.add_argument(
        "--strategy",
        required=True,
        choices=["fixed", "sentence", "paragraph"],
        help="Chunking strategy to use."
    )

    return parser.parse_args()


def index_document(file_path: str, strategy: str):
    """
    Load, chunk, embed, and store a document.
    """

    print(f"Loading document: {file_path}")

    text = load_document(file_path)

    print("Document loaded successfully.")

    chunks = chunk_text(
        text,
        strategy=strategy
    )

    if not chunks:
        raise ValueError("No chunks were created from the document.")

    print(f"Created {len(chunks)} chunks using '{strategy}' strategy.")

    initialize_database()

    filename = Path(file_path).name

    for index, chunk in enumerate(chunks, start=1):
        print(f"Processing chunk {index}/{len(chunks)}...")

        embedding = create_embedding(chunk)

        insert_chunk(
            chunk_text=chunk,
            embedding=embedding,
            filename=filename,
            split_strategy=strategy
        )

    print()
    print("Indexing completed successfully.")
    print(f"File: {filename}")
    print(f"Strategy: {strategy}")
    print(f"Chunks stored: {len(chunks)}")


def main():
    args = parse_arguments()

    try:
        index_document(
            file_path=args.file,
            strategy=args.strategy
        )

    except FileNotFoundError as error:
        print(f"File error: {error}")

    except ValueError as error:
        print(f"Input error: {error}")

    except ConnectionError as error:
        print(f"Database connection error: {error}")

    except RuntimeError as error:
        print(f"Processing error: {error}")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()