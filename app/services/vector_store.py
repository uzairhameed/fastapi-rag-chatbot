from qdrant_client import QdrantClient, models
from uuid import uuid4

from app.config import TOP_K

# Initialize local Qdrant storae

client= QdrantClient(path="qdrant_data")

COLLECTION_NAME= "documents"
VECTOR_SIZE =384

# Create the collection if it does not already exist.

def create_collection():
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE
            )
        )

def store_chunks(
        chunks: list[str],
        embeddings: list[list[float]],
        filename: str
):
    """
    Store text chunks, vectors, and metadata in Qdrant.
    """
    points =[]

    for index,(chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        points.append(
            models.PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "source": filename,
                    "chunk_index": index
                }
            )
        )
    client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

def search_chunks(query_embedding: list [float])->list[dict]:
     """
    Search Qdrant and return the top relevant chunks.
    """
     results=client.query_points(
         collection_name=COLLECTION_NAME,
         query=query_embedding,
         limit=TOP_K,
         with_payload=True
     ).points

     return [
         {
             "text": result.payload["text"],
             "source": result.payload["source"],
             "chunk_index": result.payload["chunk_index"],
             "score":result.score
         }
         for result in results
     ]