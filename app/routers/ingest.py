from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas import IngestResponse
from app.services.chunking import extract_text, chunk_text
from app.services.embeddings import generate_embedding
from app.services.vector_store import create_collection, store_chunks

router=APIRouter()

@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(file: UploadFile=File(...)):

    # Validate file extension
    if not file.filename.lower().endswith((".txt",".pdf")):
        raise HTTPException(
            status_code=400,
            detail="Only TXT and PDF files are supported."
        )

    try:

        # 1.Read Uploaded file
        file_bytes= await file.read()

        # 2.Extract text
        text= extract_text(file_bytes, file.filename)

        # 3.Split text into chunks
        chunks= chunk_text(text)

        # 4.Generate embeddings
        embeddings=generate_embedding(chunks)

        # 5.Create Qdrant collection if needed
        create_collection()

        # 6.Store chunks and metadata in Qdrant
        store_chunks(chunks, embeddings, file.filename)

        return IngestResponse(
            message="Document ingested successfully",
            filename=file.filename,
            chunks_created=len(chunks)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Document ingestion failed: {str(error)}"
        )

