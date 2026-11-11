from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL

# Load the model
model=SentenceTransformer(EMBEDDING_MODEL)

# Convert a list of text chunks into embedding vectors


def generate_embeddings(texts: list[str])-> list[list[float]]:

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings.tolist()

# Convert a single query into an embedding vector.
  
def generate_embedding(text: str) -> list[float]:

    embedding=model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding.tolist()


