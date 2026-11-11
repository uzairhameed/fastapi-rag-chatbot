
from app.services.chunking import chunk_text


def test_short_text_creates_one_chunk():
    text = "FastAPI is a Python web framework."

    chunks = chunk_text(text)

    assert len(chunks) == 1
    assert chunks[0] == text


def test_long_text_creates_multiple_chunks():
    text = "A" * 1200

    chunks = chunk_text(text)

    assert len(chunks) == 3
    assert len(chunks[0]) == 500
    assert len(chunks[1]) == 500
    assert len(chunks[2]) == 300


def test_chunks_have_correct_overlap():
    text = "A" * 1200

    chunks = chunk_text(text)

    assert chunks[0][-50:] == chunks[1][:50]
    assert chunks[1][-50:] == chunks[2][:50]


def test_empty_text_returns_no_chunks():
    text = ""

    chunks = chunk_text(text)

    assert chunks == []
