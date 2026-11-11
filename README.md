# FastAPI RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with **FastAPI, Groq GPT-OSS-120B, Qdrant, and Sentence Transformers**. It allows users to upload PDF and TXT documents, ask questions based on their content, maintain conversation history, and receive AI-generated responses through real-time streaming.

## Features

- **Document Ingestion:** Upload and process PDF and TXT documents.
- **Text Extraction:** Extract text from uploaded documents.
- **Text Chunking:** Split documents into smaller overlapping chunks for better retrieval.
- **Local Embeddings:** Generate vector embeddings using `all-MiniLM-L6-v2`.
- **Vector Database:** Store and retrieve document embeddings using Qdrant.
- **Semantic Search:** Retrieve the most relevant document chunks based on user queries.
- **LLM Integration:** Generate context-aware responses using Groq's GPT-OSS-120B model.
- **Conversation Memory:** Maintain session-based conversation history with the latest six conversation turns.
- **Response Caching:** Cache responses using SHA256-based cache keys to reduce repeated LLM API calls.
- **Streaming Responses:** Stream generated responses incrementally using FastAPI's `StreamingResponse`.
- **Grounded Responses:** Instruct the LLM to answer using retrieved document context and acknowledge when information is unavailable.
- **Automated Testing:** Test ingestion, chat, caching, chunking, and conversation memory using Pytest.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Backend development |
| FastAPI | REST API framework |
| Groq API | LLM inference |
| GPT-OSS-120B | Language model |
| Sentence Transformers | Text embeddings |
| all-MiniLM-L6-v2 | Embedding model |
| Qdrant | Vector database |
| PyPDF | PDF text extraction |
| Pytest | Automated testing |
| Uvicorn | ASGI server |

## Architecture

The application follows a modular architecture that separates API routes, business logic, and external integrations.

```text
                 User
                   |
                   v
              FastAPI API
                   |
          +--------+--------+
          |                 |
          v                 v
      Ingestion          Chat API
          |                 |
          v                 v
     Text Extraction    Query Embedding
          |                 |
          v                 v
      Text Chunking     Qdrant Search
          |                 |
          v                 v
      Embeddings       Retrieved Chunks
          |                 |
          v                 v
        Qdrant <-------- Context
                            |
                            v
                     Conversation History
                            |
                            v
                       Groq LLM
                            |
                  +---------+---------+
                  |                   |
                  v                   v
               /chat             /chat/stream
             JSON response       Streaming response
```

## Project Structure

```text
rag-chatbot/
│
├── app/
│   ├── routers/
│   │   ├── ingest.py
│   │   └── chat.py
│   │
│   ├── services/
│   │   ├── cache.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── llm.py
│   │   ├── memory.py
│   │   ├── prompts.py
│   │   └── vector_store.py
│   │
│   ├── config.py
│   └── schemas.py
│
├── tests/
│   ├── fixtures/
│   │   ├── sample.txt
│   │   └── sample.pdf
│   │
│   ├── conftest.py
│   ├── test_cache.py
│   ├── test_chat.py
│   ├── test_chunking.py
│   ├── test_ingest.py
│   └── test_memory.py
│
├── main.py
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/uzairhameed/fastapi-rag-chatbot.git

cd fastapi-rag-chatbot
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows Git Bash:

```bash
source .venv/Scripts/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

You can obtain your API key from the [Groq Console](https://console.groq.com/).

Never commit your actual `.env` file or API key to GitHub.

### 5. Run the application

```bash
python -m uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### 1. Ingest Documents

**Endpoint:** `POST /ingest`

Upload a PDF or TXT document for processing and indexing.

Example:

```bash
curl -X POST http://127.0.0.1:8000/ingest \
-F "file=@tests/fixtures/sample.pdf"
```

The ingestion process:

1. Extracts text from the uploaded file.
2. Splits the text into overlapping chunks.
3. Generates embeddings locally.
4. Stores vectors and associated metadata in Qdrant.

### 2. Chat

**Endpoint:** `POST /chat`

Ask questions about uploaded documents and receive a complete JSON response.

Example:

```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{
    "session_id": "session-123",
    "query": "Summarize the PDF."
}'
```

Example response:

```json
{
    "answer": "The document describes a Python training program and its capstone project...",
    "sources": [
        "sample.pdf"
    ]
}
```

### 3. Streaming Chat

**Endpoint:** `POST /chat/stream`

Receive the generated response incrementally instead of waiting for the complete answer.

Example:

```bash
curl -N -X POST http://127.0.0.1:8000/chat/stream \
-H "Content-Type: application/json" \
-d '{
    "session_id": "session-123",
    "query": "Summarize the PDF."
}'
```

The `-N` option disables curl's output buffering so streamed content can be displayed as it arrives.

## Configuration

The main application settings are maintained in `app/config.py`.

| Setting | Value |
|---|---|
| LLM Model | `openai/gpt-oss-120b` |
| Embedding Model | `all-MiniLM-L6-v2` |
| Embedding Dimensions | 384 |
| Chunk Size | 500 characters |
| Chunk Overlap | 50 characters |
| Retrieval Top K | 3 |
| Conversation History | Latest 6 turns |

## Response Caching

The application uses an in-memory Python dictionary to cache generated responses.

Cache keys are generated using:

- Session ID
- SHA256 hash of the normalized query

This allows the application to reuse previously generated responses for repeated questions within the same session.

## Conversation Memory

Conversation history is maintained using session IDs.

The application stores user and assistant messages and provides the latest six conversation turns (up to twelve messages) to the LLM as context.

## Running Tests

Run the automated test suite from the project root:

```bash
pytest -v
```

The tests cover:

- PDF and TXT document ingestion.
- Chat response generation.
- Handling questions without sufficient document context.
- Source identification and deduplication.
- Response caching.
- Text chunking and overlap.
- Conversation history and session isolation.

## Current Limitations

- Qdrant uses local persistent storage.
- Response caching is in-memory and does not persist after application restarts.
- Conversation history is maintained in application memory and is not persistent across restarts.
- The application currently supports PDF and TXT ingestion.
- The chatbot's answers depend on the quality and relevance of retrieved document chunks.

## Future Improvements

- Persistent conversation storage using PostgreSQL.
- Redis-based distributed response caching.
- Support for additional document formats.
- Authentication and user management.
- Docker-based deployment.
- Cloud deployment and CI/CD integration.
- Improved retrieval using reranking techniques.

## Learning Outcomes

This project provided hands-on experience with:

- Building modular REST APIs using FastAPI.
- Implementing a Retrieval-Augmented Generation pipeline.
- Working with vector databases and semantic search.
- Generating embeddings using Sentence Transformers.
- Integrating hosted LLM inference through Groq.
- Implementing conversation memory and response caching.
- Building real-time streaming API endpoints.
- Writing automated tests using Pytest.

## License

This project is open source. Add a license file if you intend to distribute it under a specific license.