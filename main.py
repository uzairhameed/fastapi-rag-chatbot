from fastapi import FastAPI

from app.routers import chat, ingest

app= FastAPI(
    title="RAG Chatbot API",
    description="A document-based chatbot using Groq, Sentence Transformers, and Qdrant.",
    version="1.0.0"
)

# Register API routers

app.include_router(ingest.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return{
        "message": "RAG Chatbot API is running"
    }
