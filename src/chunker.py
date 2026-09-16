import re


def split_fixed_size(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into fixed-size character chunks with overlap.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def split_sentences(text: str, sentences_per_chunk: int = 3) -> list[str]:
    """
    Split text into chunks based on sentences.
    """
    if sentences_per_chunk <= 0:
        raise ValueError("sentences_per_chunk must be greater than 0.")

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    chunks = []

    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = " ".join(sentences[i:i + sentences_per_chunk])
        chunks.append(chunk)

    return chunks


def split_paragraphs(text: str) -> list[str]:
    """
    Split text based on paragraph boundaries.
    """
    paragraphs = re.split(r'\n\s*\n', text)

    return [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]


def chunk_text(
    text: str,
    strategy: str,
    chunk_size: int = 500,
    overlap: int = 50,
    sentences_per_chunk: int = 3
) -> list[str]:
    """
    Split text using the requested strategy.
    """

    strategy = strategy.lower()

    if strategy == "fixed":
        return split_fixed_size(
            text,
            chunk_size=chunk_size,
            overlap=overlap
        )

    if strategy == "sentence":
        return split_sentences(
            text,
            sentences_per_chunk=sentences_per_chunk
        )

    if strategy == "paragraph":
        return split_paragraphs(text)

    raise ValueError(
        f"Unsupported split strategy: {strategy}. "
        "Supported strategies are: fixed, sentence, paragraph."
    )