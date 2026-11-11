from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.services.prompts import SYSTEM_PROMPT, build_prompt

# Intialize Groq client once
client = Groq(api_key=GROQ_API_KEY)

def generate_response(
        query: str,
        retrieved_chunks: list[dict],
        conversation_history: list[dict]
)-> str:
    
    """
    Generate a complete response using Groq.
    """
    user_prompt= build_prompt(query,retrieved_chunks)

    messages=[
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # Include previous conversation turns
    messages.extend(conversation_history)

    # Add the current question and retrieved context

    messages.append({
        "role": "user",
        "content": user_prompt
    })

    response=client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content or ""

def stream_response(
        query: str,
        retrieved_chunks: list[dict],
        conversation_history: list[dict]
):
    """
    Generate a streaming response using Groq.
    """
    user_prompt = build_prompt(query, retrieved_chunks)

    messages=[
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    messages.extend(conversation_history)

    messages.append({
        "role": "user",
        "content": user_prompt
    })

    stream=client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0,
        stream=True
    )

    for chunk in stream:
        content= chunk.choices[0].delta.content

        if content:
            yield content