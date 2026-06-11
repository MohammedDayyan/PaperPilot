from fastapi import APIRouter, HTTPException, Header
from typing import Optional

import services.supabase_service as db
from api.deps import get_user_id
from agents.flashcard_agent import generate_flashcards

router = APIRouter()


@router.get("/{paper_id}/flashcards")
async def get_flashcards(paper_id: str, authorization: Optional[str] = Header(None)):
    """Fetch flashcards for a specific paper if they have been generated."""
    user_id = get_user_id(authorization)

    paper = db.select_one("papers", {"id": paper_id, "user_id": user_id})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    record = db.select_one("flashcards", {"paper_id": paper_id})
    return {"cards": record.get("cards") if record else None}


@router.post("/{paper_id}/flashcards")
async def create_flashcards(paper_id: str, authorization: Optional[str] = Header(None)):
    """Generate flashcards from the AI report and persist them."""
    user_id = get_user_id(authorization)

    paper = db.select_one("papers", {"id": paper_id, "user_id": user_id})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    existing = db.select_one("flashcards", {"paper_id": paper_id})
    if existing:
        return {"cards": existing.get("cards"), "message": "Flashcards already exist"}

    report = db.select_one("reports", {"paper_id": paper_id})
    if not report or not report.get("report_text"):
        raise HTTPException(status_code=400, detail="AI Report not found. Please summarize the paper first.")

    try:
        cards_data = generate_flashcards(report["report_text"])
        db.insert("flashcards", {"paper_id": paper_id, "cards": cards_data})
        return {"cards": cards_data, "message": "Flashcards generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Flashcard generation failed: {str(e)}")


@router.delete("/{paper_id}/flashcards")
async def delete_flashcards(paper_id: str, authorization: Optional[str] = Header(None)):
    """Delete flashcards for a specific paper to allow regeneration."""
    user_id = get_user_id(authorization)

    # Verify ownership
    paper = db.select_one("papers", {"id": paper_id, "user_id": user_id})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    db.delete_row("flashcards", {"paper_id": paper_id})
    return {"message": "Flashcards deleted successfully"}
