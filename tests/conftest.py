import pytest
from fastapi.testclient import TestClient

from main import app
from app.services.memory import conversation_store
from app.services.cache import response_cache


@pytest.fixture
def client():
    # Clear previous test data
    conversation_store.clear()
    response_cache.clear()

    with TestClient(app) as test_client:
        yield test_client