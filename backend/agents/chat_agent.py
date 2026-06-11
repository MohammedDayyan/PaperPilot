from services.groq_service import chat_completion


def answer_question(question: str, context_chunks: list[str], history: list[dict]) -> str:
    """
    RAG Chat Agent — answers a user's question about the paper using retrieved context chunks
    and chat history.
    """
    context_text = "\n\n".join(f"- Chunk {i+1}: {chunk}" for i, chunk in enumerate(context_chunks))

    system_prompt = f"""You are an expert AI academic research assistant. You help the user understand a scientific paper by answering their questions using the provided context chunks from the paper.

Context Chunks from the Paper:
{context_text}

Guidelines:
1. Base your answer primarily on the provided context chunks.
2. If the answer is not in the context, use your general academic knowledge but clearly state that it is not explicitly mentioned in the paper's summary.
3. Be professional, academic, clear, and concise. Use markdown formatting (like bolding, bullet points, and code blocks) where appropriate.
4. Keep the response focused on the user's question.
"""

    messages = [{"role": "system", "content": system_prompt}]

    # Add recent history (up to last 4 exchanges to keep context clean and avoid token limits)
    # Each history item is a dict: {"question": "...", "answer": "..."}
    for exchange in history[-4:]:
        messages.append({"role": "user", "content": exchange.get("question", "")})
        messages.append({"role": "assistant", "content": exchange.get("answer", "")})

    messages.append({"role": "user", "content": question})

    answer = chat_completion(
        messages=messages,
        temperature=0.5,
        max_tokens=1024,
    )
    return answer
