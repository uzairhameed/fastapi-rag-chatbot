from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas import ChatRequest, ChatResponse

from app.services.embeddings import generate_embedding
from app.services.vector_store import create_collection, search_chunks
from app.services.llm import generate_response,stream_response
from app.services.memory import get_history, add_message
from app.services.cache import get_cached_response,cache_response

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        create_collection()

        query_embedding = generate_embedding(request.query)
        retrieved_chunks = search_chunks(query_embedding)

        answer = get_cached_response(
            request.session_id,
            request.query
        )

        if answer is None:
            history = get_history(request.session_id)

            print("Session ID:", request.session_id)
            print("Conversation history:", history)

            answer = generate_response(
                request.query,
                retrieved_chunks,
                history
            )

            cache_response(
                request.session_id,
                request.query,
                answer
            )

        # Update history whether cache hits or misses
        add_message(request.session_id, "user", request.query)
        add_message(request.session_id, "assistant", answer)

        sources = list(dict.fromkeys(
            chunk["source"] for chunk in retrieved_chunks
        ))

        return ChatResponse(
            answer=answer,
            sources=sources
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Chat request failed: {str(error)}"
        )

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    try:
        create_collection()

        query_embedding = generate_embedding(request.query)
        retrieved_chunks = search_chunks(query_embedding)

        cached_answer = get_cached_response(
            request.session_id,
            request.query
        )

        history = get_history(request.session_id)

        def generate():
            if cached_answer is not None:
                answer = cached_answer
                yield answer
            else:
                response_parts = []

                for token in stream_response(
                    request.query,
                    retrieved_chunks,
                    history
                ):
                    response_parts.append(token)
                    yield token

                answer = "".join(response_parts)

                cache_response(
                    request.session_id,
                    request.query,
                    answer
                )

            add_message(request.session_id, "user", request.query)
            add_message(request.session_id, "assistant", answer)

        return StreamingResponse(
            generate(),
            media_type="text/plain"
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Streaming chat failed: {str(error)}"
        )


