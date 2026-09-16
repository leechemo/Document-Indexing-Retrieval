import psycopg

from src.config import POSTGRES_URL


EMBEDDING_DIMENSION = 3072


def get_connection():
    if not POSTGRES_URL:
        raise ValueError("POSTGRES_URL is missing from the .env file.")

    try:
        return psycopg.connect(POSTGRES_URL)

    except psycopg.Error as error:
        raise ConnectionError(
            f"Failed to connect to PostgreSQL: {error}"
        ) from error


def initialize_database():
    create_extension_query = """
        CREATE EXTENSION IF NOT EXISTS vector;
    """

    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id SERIAL PRIMARY KEY,
            chunk_text TEXT NOT NULL,
            embedding VECTOR({EMBEDDING_DIMENSION}) NOT NULL,
            filename TEXT NOT NULL,
            split_strategy VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(create_extension_query)
                cursor.execute(create_table_query)

            connection.commit()

    except psycopg.Error as error:
        raise RuntimeError(
            f"Failed to initialize database: {error}"
        ) from error


def insert_chunk(
    chunk_text: str,
    embedding: list[float],
    filename: str,
    split_strategy: str
):
    query = """
        INSERT INTO document_chunks
            (chunk_text, embedding, filename, split_strategy)
        VALUES
            (%s, %s, %s, %s);
    """

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        chunk_text,
                        embedding,
                        filename,
                        split_strategy
                    )
                )

            connection.commit()

    except psycopg.Error as error:
        raise RuntimeError(
            f"Failed to insert chunk into database: {error}"
        ) from error


def search_similar_chunks(
    query_embedding: list[float],
    limit: int = 3,
    strategy: str | None = None
):
    """
    Search for the most semantically similar document chunks
    using cosine distance.

    Optionally filter by chunking strategy.
    """

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:

                if strategy:
                    query = """
                        SELECT
                            id,
                            chunk_text,
                            filename,
                            split_strategy,
                            1 - (embedding <=> %s::vector) AS similarity
                        FROM document_chunks
                        WHERE split_strategy = %s
                        ORDER BY embedding <=> %s::vector
                        LIMIT %s;
                    """

                    cursor.execute(
                        query,
                        (
                            query_embedding,
                            strategy,
                            query_embedding,
                            limit
                        )
                    )

                else:
                    query = """
                        SELECT
                            id,
                            chunk_text,
                            filename,
                            split_strategy,
                            1 - (embedding <=> %s::vector) AS similarity
                        FROM document_chunks
                        ORDER BY embedding <=> %s::vector
                        LIMIT %s;
                    """

                    cursor.execute(
                        query,
                        (
                            query_embedding,
                            query_embedding,
                            limit
                        )
                    )

                results = cursor.fetchall()

        return results

    except psycopg.Error as error:
        raise RuntimeError(
            f"Failed to perform semantic search: {error}"
        ) from error