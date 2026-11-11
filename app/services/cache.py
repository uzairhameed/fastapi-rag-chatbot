import hashlib

# In-memory response cache
response_cache: dict[str, str]={}

def generate_cache_key(session_id: str, query: str)-> str:
    """
    Generate a unique cache key using session ID and SHA256 query hash.
    """

    query_hash=hashlib.sha256(
        query.strip().encode("utf-8")
    ).hexdigest()

    return f"{session_id}:{query_hash}"

def get_cached_response(session_id: str, query: str)->str | None:
    """
    Retrieve a cached response if available.
    """
    cache_key = generate_cache_key(session_id, query)

    return response_cache.get(cache_key)

def cache_response(session_id: str, query: str, answer: str):
    """
    Store a generated response in the cache.
    """
    cache_key= generate_cache_key(session_id, query)
    response_cache[cache_key]= answer


