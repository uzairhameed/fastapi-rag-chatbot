from app.config import MAX_HISTORY_TURNS

# Store conversation history separately for each session

conversation_store:dict[str,list[dict]]={}

def get_history(session_id: str)-> list[dict]:
    """
    Retrieve the last 6 conversation turns for a session.
    """
    history= conversation_store.get(session_id,[])

    # Each turn contains 2 messages:
    # 1 user message + 1 assistant message
    return history[-(MAX_HISTORY_TURNS * 2):]

def add_message(
        session_id: str,
        role: str,
        content: str
):
    """
    Add a user or assistant message to session history.
    """
    if session_id not in conversation_store:
        conversation_store[session_id]=[]

    conversation_store[session_id].append({
        "role": role,
        "content": content
    })

def clear_history(session_id: str):
     """
    Clear conversation history for a session.
    """
     conversation_store.pop(session_id, None)