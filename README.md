# Document Indexing & Semantic Retrieval

This project implements a document indexing and semantic search pipeline using Python, Gemini embeddings, PostgreSQL, and pgvector.

The system supports PDF and DOCX files, extracts clean text, splits documents into chunks using multiple strategies, generates embeddings with `gemini-embedding-001`, stores them in PostgreSQL, and performs semantic similarity search.

## Features

- PDF and DOCX text extraction
- Clean text preprocessing
- Three chunking strategies:
  - Fixed-size chunks with overlap
  - Sentence-based chunks
  - Paragraph-based chunks
- Gemini embeddings using `gemini-embedding-001`
- PostgreSQL storage with pgvector
- Semantic similarity search using cosine distance
- Optional search filtering by chunking strategy
- Error handling for missing files, unsupported file types, documents with no extractable text, embedding failures, database connection failures, and empty search results

## Project Structure

```text
jeen-part2/
│
├── index_documents.py
├── search.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── docs/
│
└── src/
    ├── __init__.py
    ├── config.py
    ├── document_loader.py
    ├── chunker.py
    ├── embeddings.py
    └── database.py
```

# Requirements

Before running the project, make sure the following are installed:

- Python 3.10+
- PostgreSQL
- pgvector extension
- Gemini API key

# Installation

## 1. Create a Virtual Environment

```bash
python -m venv venv
```

## 2. Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key
POSTGRES_URL=postgresql://postgres:your_password@localhost:5432/jeen_documents
```

Do not commit the `.env` file to GitHub.

The `.env.example` file can be used as a template.

# PostgreSQL Setup

## 1. Create the Database

Create a PostgreSQL database, for example:

```text
jeen_documents
```

## 2. Enable pgvector

Run the following command inside the database:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## 3. Database Table

The application automatically creates the `document_chunks` table when indexing a document.

The table contains the following fields:

- `id`
- `chunk_text`
- `embedding`
- `filename`
- `split_strategy`
- `created_at`

# Document Indexing

The indexing process follows this pipeline:

```text
PDF / DOCX
    ↓
Text extraction
    ↓
Text cleaning
    ↓
Chunking
    ↓
Gemini embeddings
    ↓
PostgreSQL + pgvector
```

## Paragraph-Based Chunking

Run:

```bash
python index_documents.py --file ./docs/test.docx --strategy paragraph
```

Example output:

```text
Loading document: ./docs/test.docx
Document loaded successfully.
Created 4 chunks using 'paragraph' strategy.
Processing chunk 1/4...
Processing chunk 2/4...
Processing chunk 3/4...
Processing chunk 4/4...

Indexing completed successfully.
File: test.docx
Strategy: paragraph
Chunks stored: 4
```

## Sentence-Based Chunking

Run:

```bash
python index_documents.py --file ./docs/test.docx --strategy sentence
```

The current implementation groups three sentences into each chunk.

## Fixed-Size Chunking

Run:

```bash
python index_documents.py --file ./docs/test.docx --strategy fixed
```

Default configuration:

```text
Chunk size: 500 characters
Overlap: 50 characters
```

# Chunking Strategies

## Fixed-Size with Overlap

The text is divided into chunks of a fixed number of characters.

A configurable overlap is preserved between neighboring chunks in order to maintain context across chunk boundaries.

Default values:

```text
Chunk size: 500 characters
Overlap: 50 characters
```

## Sentence-Based Splitting

The text is split into sentences.

The current implementation groups three sentences into each chunk.

This creates smaller and more focused semantic units compared to paragraph-based chunking.

## Paragraph-Based Splitting

The extracted text is split according to paragraph boundaries.

Each paragraph becomes a separate chunk.

This strategy preserves the original paragraph structure of the document.

# Gemini Embeddings

Document chunks are converted into embeddings using:

```text
gemini-embedding-001
```

For document chunks, the system generates embeddings using the `RETRIEVAL_DOCUMENT` task type.

For user search queries, the system generates embeddings using the `RETRIEVAL_QUERY` task type.

The generated embeddings contain 3072 dimensions and are stored in PostgreSQL using pgvector.

# Semantic Search

Semantic search converts the user's query into an embedding and compares it with the embeddings stored in PostgreSQL.

The system uses cosine distance through pgvector and returns the most semantically similar chunks first.

## Basic Search

```bash
python search.py --query "What happened to Michael Jackson in 2009?"
```

## Search by Chunking Strategy

Search only sentence-based chunks:

```bash
python search.py --query "What happened to Michael Jackson in 2009?" --strategy sentence
```

Search only paragraph-based chunks:

```bash
python search.py --query "What happened to Michael Jackson in 2009?" --strategy paragraph
```

## Limit the Number of Results

```bash
python search.py --query "Michael Jackson albums" --limit 5
```

# Example Search Result

Example command:

```bash
python search.py --query "What happened to Michael Jackson in 2009?" --strategy sentence
```

Example output:

```text
Searching for: "What happened to Michael Jackson in 2009?"

Top 3 results:
======================================================================

Result 1
Similarity: 0.7528
File: test.docx
Strategy: sentence
Text:
His death caused unprecedented surges in internet traffic and a spike in music sales. Posthumous Jackson releases include the documentary Michael Jackson's This Is It (2009) and the albums Michael (2010) and Xscape (2014). The 2019 documentary Leaving Neverland detailed further child sexual abuse allegations against Jackson.
----------------------------------------------------------------------

Result 2
Similarity: 0.7422
File: test.docx
Strategy: sentence
Text:
He was accused of sexually abusing a child in 1993 and settled out of court in 1994. In 2005, he was tried and acquitted on other child sexual abuse charges. While preparing for This Is It, a series of comeback concerts, he died in 2009 from an overdose of propofol administered by his personal physician, Conrad Murray.
----------------------------------------------------------------------

Result 3
Similarity: 0.7090
File: test.docx
Strategy: sentence
Text:
Michael Joseph Jackson (August 29, 1958 – June 25, 2009) was an American singer, songwriter, dancer, and philanthropist. Dubbed the "King of Pop", Jackson is widely regarded as one of the most culturally significant figures of the 20th century. His musical achievements broke American racial barriers and made him a dominant figure worldwide.
```

# Error Handling

The application handles the main failure scenarios required by the assignment.

## Missing File

Example:

```text
File error: File not found: ./docs/not_exist.pdf
```

## Unsupported File Type

Example:

```text
Input error: Unsupported file type: .txt.
```

## Document with No Extractable Text

Example:

```text
Input error: No extractable text found in document.
```

## Embedding Failure

Gemini API failures are caught and returned as readable processing errors.

## Database Connection Failure

PostgreSQL connection failures are caught and returned as readable database connection errors.

## Empty Search Results

If no matching records are found, the application prints:

```text
No matching results found.
```

# Security

Sensitive values are stored in the `.env` file and are not hardcoded in the source code.

The project does not print API keys or database credentials.

The `.env` file is excluded from Git using `.gitignore`.

# Example End-to-End Workflow

First, index a document:

```bash
python index_documents.py --file ./docs/test.docx --strategy paragraph
```

Then perform semantic search:

```bash
python search.py --query "What happened to Michael Jackson in 2009?"
```

The indexing command:

- Extracts text from the document
- Cleans the extracted text
- Splits the text into chunks
- Generates Gemini embeddings
- Stores the chunks and embeddings in PostgreSQL

The search command:

- Generates an embedding for the user's query
- Compares it with the stored embeddings
- Returns the most semantically similar document chunks