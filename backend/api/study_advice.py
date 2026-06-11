from fastapi import APIRouter, HTTPException, Header
from typing import Optional

import services.supabase_service as db
from api.deps import get_user_id
from agents.study_advice_agent import generate_study_advice

router = APIRouter()


@router.get("/{paper_id}/advice")
async def get_advice(paper_id: str, authorization: Optional[str] = Header(None)):
    """Fetch study advice for a specific paper if it has been generated."""
    user_id = get_user_id(authorization)

    paper = db.select_one("papers", {"id": paper_id, "user_id": user_id})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    record = db.select_one("study_advice", {"paper_id": paper_id})
    return {"advice": record.get("advice") if record else None}


@router.post("/{paper_id}/advice")
async def create_advice(paper_id: str, authorization: Optional[str] = Header(None)):
    """Generate a study guide from the AI report and persist it."""
    user_id = get_user_id(authorization)

    paper = db.select_one("papers", {"id": paper_id, "user_id": user_id})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    existing = db.select_one("study_advice", {"paper_id": paper_id})
    if existing:
        return {"advice": existing.get("advice"), "message": "Study advice already exists"}

    report = db.select_one("reports", {"paper_id": paper_id})
    if not report or not report.get("report_text"):
        raise HTTPException(status_code=400, detail="AI Report not found. Please summarize the paper first.")

    try:
        advice_text = generate_study_advice(report["report_text"])
        db.insert("study_advice", {"paper_id": paper_id, "advice": advice_text})
        return {"advice": advice_text, "message": "Study advice generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Study advice generation failed: {str(e)}")


@router.delete("/{paper_id}/advice")
async def delete_advice(paper_id: str, authorization: Optional[str] = Header(None)):
    """Delete study advice for a specific paper to allow regeneration."""
    user_id = get_user_id(authorization)

    # Verify ownership
    paper = db.select_one("papers", {"id": paper_id, "user_id": user_id})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    db.delete_row("study_advice", {"paper_id": paper_id})
    return {"message": "Study advice deleted successfully"}
