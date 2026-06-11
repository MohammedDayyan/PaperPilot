from fastapi import APIRouter, HTTPException, Header
from typing import Optional

import services.supabase_service as db
from api.deps import get_user_id
from services.rag_service import retrieve_chunks
from agents.chat_agent import answer_question

router = APIRouter()


@router.get("/{paper_id}/chat")
async def get_chat_history(paper_id: str, authorization: Optional[str] = Header(None)):
    """Fetch all chat history for a specific paper."""
    user_id = get_user_id(authorization)

    # Verify ownership
    paper = db.select_one("papers", {"id": paper_id, "user_id": user_id})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    history = db.select("chat_history", {"paper_id": paper_id})
    # Sort history by created_at in ascending order so it reads chronologically
    history.sort(key=lambda x: x.get("created_at", ""))
    return {"history": history}


@router.post("/{paper_id}/chat")
async def ask_paper_question(
    paper_id: str,
    payload: dict,
    authorization: Optional[str] = Header(None)
):
    """Ask a question about the paper, search chunks via RAG, generate answer, save history."""
    user_id = get_user_id(authorization)
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    # Verify ownership
    paper = db.select_one("papers", {"id": paper_id, "user_id": user_id})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    # Retrieve report text as the document source
    report = db.select_one("reports", {"paper_id": paper_id})
    if not report or not report.get("report_text"):
        raise HTTPException(status_code=400, detail="AI Report not found. Please summarize the paper first.")

    try:
        # Get chat history to pass to agent
        history = db.select("chat_history", {"paper_id": paper_id})
        history.sort(key=lambda x: x.get("created_at", ""))

        # Retrieve relevant chunks using RAG service
        chunks = retrieve_chunks(paper_id, report["report_text"], question, k=4)

        # Generate answer
        answer = answer_question(question, chunks, history)

        # Insert to database
        new_row = db.insert(
            "chat_history",
            {
                "paper_id": paper_id,
                "question": question,
                "answer": answer,
            }
        )

        return {"answer": answer, "message": "Answer generated successfully", "record": new_row}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")
