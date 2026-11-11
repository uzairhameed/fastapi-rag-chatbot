from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    query: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]

class IngestResponse(BaseModel):
    message: str
    filename: str
    chunks_created: int

