SYSTEM_PROMPT= """
You are a helpful document-based AI assistant.

Follow these rules strictly:

1. Use retrieved document context as the source of truth
   for factual questions about the documents.

2. Use conversation history to understand references to
   previous questions and answers.

3. If the user asks what they previously asked or discussed,
   use conversation history to answer.

4. Do not use outside knowledge or invent facts.

5. If a factual answer is not available in the retrieved
   context, respond with:
   "I don't know based on the provided documents."

6. If the context only partially answers a question,
   clearly explain what information is available.

7. Never use another session's conversation history.
"""

def build_prompt(
        query: str,
        retrieved_chunks: list[dict]
) -> str:

    context = "\n\n".join(
        f"Source: {chunk['source']}\n"
        f"Content: {chunk['text']}"
        for chunk in retrieved_chunks
    )

    prompt = f"""
Retrieved Document Context:

{context}

Current User Question:
{query}

Instructions:
- For questions about document facts, use the retrieved document context.
- For questions about previous messages, use conversation history.
- If a document-related answer is unavailable in the retrieved
  context, say: "I don't know based on the provided documents."
- Do not invent information.
"""
    return prompt