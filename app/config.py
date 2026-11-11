import os
from dotenv import load_dotenv

# Load environment variables from the root .env file
load_dotenv()

# API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# LLM configuration
GROQ_MODEL = "openai/gpt-oss-120b"

# Embedding configuration
EMBEDDING_MODEL="all-MiniLM-L6-v2"

# Document processing configuration
CHUNK_SIZE= 500
CHUNK_OVERLAP= 50

# Retrieval configuration
TOP_K = 3

# Conversation configuration
MAX_HISTORY_TURNS = 6