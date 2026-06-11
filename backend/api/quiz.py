from fastapi import APIRouter, HTTPException, Header
from typing import Optional

import services.supabase_service as db
from api.deps import get_user_id
from agents.quiz_agent import generate_quiz

router = APIRouter()


@router.get("/{paper_id}/quiz")
async def get_quiz(paper_id: str, authorization: Optional[str] = Header(None)):
    """Fetch the quiz for a specific paper if it has been generated."""
    user_id = get_user_id(authorization)

    # Verify ownership
    paper = db.select_one("papers", {"id": paper_id, "user_id": user_id})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    quiz_record = db.select_one("quizzes", {"paper_id": paper_id})
    return {"quiz": quiz_record.get("quiz") if quiz_record else None}


@router.post("/{paper_id}/quiz")
async def create_quiz(paper_id: str, authorization: Optional[str] = Header(None)):
    """Generate a new quiz using the summary report text and persist it."""
    user_id = get_user_id(authorization)

    # Verify ownership
    paper = db.select_one("papers", {"id": paper_id, "user_id": user_id})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    # Return existing if already generated
    existing = db.select_one("quizzes", {"paper_id": paper_id})
    if existing:
        return {"quiz": existing.get("quiz"), "message": "Quiz already exists"}

    # Retrieve summary text
    report = db.select_one("reports", {"paper_id": paper_id})
    if not report or not report.get("report_text"):
        raise HTTPException(status_code=400, detail="AI Report not found. Please summarize the paper first.")

    try:
        quiz_data = generate_quiz(report["report_text"])
        db.insert(
            "quizzes",
            {
                "paper_id": paper_id,
                "quiz": quiz_data,
            },
        )
        return {"quiz": quiz_data, "message": "Quiz generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quiz generation failed: {str(e)}")


@router.delete("/{paper_id}/quiz")
async def delete_quiz(paper_id: str, authorization: Optional[str] = Header(None)):
    """Delete the quiz for a specific paper to allow regeneration."""
    user_id = get_user_id(authorization)

    # Verify ownership
    paper = db.select_one("papers", {"id": paper_id, "user_id": user_id})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    db.delete_row("quizzes", {"paper_id": paper_id})
    return {"message": "Quiz deleted successfully"}
