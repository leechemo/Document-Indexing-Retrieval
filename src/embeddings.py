from google import genai
from google.genai import types

from src.config import GEMINI_API_KEY


MODEL_NAME = "gemini-embedding-001"


def get_client():
    """
    Create and return a Gemini API client.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing from the .env file.")

    return genai.Client(api_key=GEMINI_API_KEY)


def create_embedding(text: str) -> list[float]:
    """
    Generate an embedding for a single text using Gemini.
    """
    if not text or not text.strip():
        raise ValueError("Cannot create embedding for empty text.")

    try:
        client = get_client()

        response = client.models.embed_content(
            model=MODEL_NAME,
            contents=text,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT"
            ),
        )

        return response.embeddings[0].values

    except Exception as error:
        raise RuntimeError(
            f"Failed to generate embedding: {error}"
        ) from error


def create_query_embedding(query: str) -> list[float]:
    """
    Generate an embedding for a search query.
    """
    if not query or not query.strip():
        raise ValueError("Cannot create embedding for an empty query.")

    try:
        client = get_client()

        response = client.models.embed_content(
            model=MODEL_NAME,
            contents=query,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY"
            ),
        )

        return response.embeddings[0].values

    except Exception as error:
        raise RuntimeError(
            f"Failed to generate query embedding: {error}"
        ) from error