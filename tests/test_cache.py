
def test_chat_uses_cache_for_repeated_query(client, monkeypatch):
    call_count = 0

    def mock_generate_response(query, retrieved_chunks, conversation_history):
        nonlocal call_count
        call_count += 1
        return "Docker is a containerization platform."

    # Mock embedding and retrieval
    monkeypatch.setattr(
        "app.routers.chat.generate_embedding",
        lambda query: [0.0] * 384
    )

    monkeypatch.setattr(
        "app.routers.chat.search_chunks",
        lambda query_embedding: []
    )

    # Mock Groq response generation
    monkeypatch.setattr(
        "app.routers.chat.generate_response",
        mock_generate_response
    )

    request_data = {
        "session_id": "cache-session",
        "query": "What is Docker?"
    }

    # First request: should generate a new response
    first_response = client.post("/chat", json=request_data)

    assert first_response.status_code == 200
    assert call_count == 1

    # Second request: should use the cached response
    second_response = client.post("/chat", json=request_data)

    assert second_response.status_code == 200
    assert call_count == 1

    assert first_response.json()["answer"] == second_response.json()["answer"]
