
def test_chat_returns_answer_and_sources(client, monkeypatch):

    # First, ingest the sample document
    with open("tests/fixtures/sample.txt", "rb") as file:
        ingest_response = client.post(
            "/ingest",
            files={
                "file": ("sample.txt", file, "text/plain")
            }
        )

    assert ingest_response.status_code == 200

    # Mock Qdrant retrieval
    mock_chunks = [ 
    {
        "text": "FastAPI is a modern Python web framework.",
        "source": "sample.txt",
        "chunk_index": 0,
        "score": 0.95
    }
]

    monkeypatch.setattr(
    "app.routers.chat.search_chunks",
    lambda query_embedding: mock_chunks
    )

    # Mock Groq so this test doesn't make a real API call
    def mock_generate_response(query, retrieved_chunks, conversation_history):
        assert len(retrieved_chunks) > 0
        return "The document was successfully ingested."

    monkeypatch.setattr(
        "app.routers.chat.generate_response",
        mock_generate_response
    )

    # Send a question to the chatbot
    response = client.post(
        "/chat",
        json={
            "session_id": "test-session",
            "query": "What information is available in the document?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == "The document was successfully ingested."
    assert "sample.txt" in data["sources"]

def test_chat_returns_dont_know_when_answer_unavailable(client, monkeypatch):
    # Mock retrieval to return no relevant chunks
    monkeypatch.setattr(
        "app.routers.chat.search_chunks",
        lambda query_embedding: []
    )

    # Mock Groq response
    monkeypatch.setattr(
        "app.routers.chat.generate_response",
        lambda query, retrieved_chunks, history:
            "I don't know based on the provided documents."
    )

    response = client.post(
        "/chat",
        json={
            "session_id": "unknown-session",
            "query": "What is the capital of Mars?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "I don't know" in data["answer"]
    assert data["sources"] == []

def test_chat_returns_correct_sources(client, monkeypatch):
    # Mock retrieved document chunks
    mock_chunks = [
        {
            "text": "FastAPI is a Python web framework.",
            "source": "fastapi-guide.txt",
            "chunk_index": 0,
            "score": 0.95
        },
        {
            "text": "Docker packages applications into containers.",
            "source": "docker-guide.txt",
            "chunk_index": 0,
            "score": 0.90
        },
        {
            "text": "FastAPI supports asynchronous endpoints.",
            "source": "fastapi-guide.txt",
            "chunk_index": 1,
            "score": 0.85
        }
    ]

    monkeypatch.setattr(
        "app.routers.chat.search_chunks",
        lambda query_embedding: mock_chunks
    )

    monkeypatch.setattr(
        "app.routers.chat.generate_response",
        lambda query, retrieved_chunks, history: "FastAPI is a Python web framework."
    )

    response = client.post(
        "/chat",
        json={
            "session_id": "source-session",
            "query": "What is FastAPI?"
        }
    )

    print("CHAT RESPONSE:", response.json())
    assert response.status_code == 200

    data = response.json()

    assert data["sources"] == [
        "fastapi-guide.txt",
        "docker-guide.txt"
    ]