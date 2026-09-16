from pathlib import Path
import re

from pypdf import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def clean_text(text: str) -> str:
    """
    Clean extracted document text.

    - Removes excessive whitespace
    - Normalizes spaces
    - Preserves paragraph breaks
    """
    if not text:
        return ""

    # Normalize Windows/Mac line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove extra spaces/tabs inside lines
    text = re.sub(r"[ \t]+", " ", text)

    # Remove spaces around newlines
    text = re.sub(r" *\n *", "\n", text)

    # Replace 3+ consecutive newlines with 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_pdf_text(file_path: Path) -> str:
    """
    Extract text from a PDF file.
    """
    reader = PdfReader(str(file_path))

    pages_text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            pages_text.append(page_text)

    return "\n\n".join(pages_text)


def extract_docx_text(file_path: Path) -> str:
    """
    Extract text from a DOCX file.
    """
    document = Document(str(file_path))

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n\n".join(paragraphs)


def load_document(file_path: str) -> str:
    """
    Load a PDF or DOCX file and return cleaned text.

    Raises:
        FileNotFoundError: File does not exist.
        ValueError: Unsupported file type or no extractable text.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            f"Supported types are: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    if extension == ".pdf":
        text = extract_pdf_text(path)

    elif extension == ".docx":
        text = extract_docx_text(path)

    else:
        raise ValueError(f"Unsupported file type: {extension}")

    text = clean_text(text)

    if not text:
        raise ValueError(
            f"No extractable text found in document: {path.name}"
        )

    return text