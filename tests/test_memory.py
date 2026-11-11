from app.services.memory import (
    add_message,
    get_history,
    clear_history,
    conversation_store
)


def test_add_and_get_conversation_history():
    session_id = "memory-test-session"

    clear_history(session_id)

    add_message(session_id, "user", "What is Docker?")
    add_message(
        session_id,
        "assistant",
        "Docker is a containerization platform."
    )

    history = get_history(session_id)

    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"
    assert history[0]["content"] == "What is Docker?"


def test_history_returns_only_last_six_turns():
    session_id = "history-limit-session"

    clear_history(session_id)

    # Add seven complete conversation turns
    for i in range(1, 8):
        add_message(session_id, "user", f"Question {i}")
        add_message(session_id, "assistant", f"Answer {i}")

    history = get_history(session_id)

    assert len(history) == 12

    # The first turn should have been excluded
    assert history[0]["content"] == "Question 2"
    assert history[1]["content"] == "Answer 2"

    # The latest turn should still be available
    assert history[-2]["content"] == "Question 7"
    assert history[-1]["content"] == "Answer 7"


def test_conversation_history_is_isolated_between_sessions():
    session_a = "user-session-A"
    session_b = "user-session-B"

    clear_history(session_a)
    clear_history(session_b)

    add_message(session_a, "user", "What is Kubernetes?")
    add_message(session_a, "assistant", "Kubernetes is a container orchestration platform.")

    add_message(session_b, "user", "What is Docker?")

    history_a = get_history(session_a)
    history_b = get_history(session_b)

    assert len(history_a) == 2
    assert len(history_b) == 1

    assert history_a[0]["content"] == "What is Kubernetes?"
    assert history_b[0]["content"] == "What is Docker?"

    assert all(
        message["content"] != "What is Kubernetes?"
        for message in history_b
    )
