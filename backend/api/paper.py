import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Header
from typing import Optional

import services.supabase_service as db
import services.storage_service as storage
from agents.reader_agent import read_paper
from agents.summary_agent import summarize_paper
from agents.report_agent import generate_report_pdf
from api.deps import get_user_id

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_paper(
    file: UploadFile = File(...),
    authorization: Optional[str] = Header(None),
):
    """
    Upload a PDF → run Reader → Summary → Report pipeline → store results.
    Returns the new paper_id and title.
    """
    user_id = get_user_id(authorization)

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    paper_id = str(uuid.uuid4())
    local_path = UPLOAD_DIR / f"{paper_id}.pdf"

    # Read the file into memory once
    content = await file.read()

    # Save a temporary local copy for PyMuPDF
    with open(local_path, "wb") as f:
        f.write(content)

    try:
        # 1. Upload original PDF to Supabase Storage
        file_url = storage.upload_file(
            storage.PAPERS_BUCKET,
            f"{user_id}/{paper_id}.pdf",
            content,
        )

        # 2. Agent pipeline
        paper_data = read_paper(str(local_path))
        summary_data = summarize_paper(paper_data)
        report_pdf_bytes = generate_report_pdf(summary_data)

        # 3. Upload generated report PDF
        report_url = storage.upload_file(
            storage.REPORTS_BUCKET,
            f"{user_id}/{paper_id}_report.pdf",
            report_pdf_bytes,
        )

        # 4. Persist to database
        title = paper_data.get("title") or file.filename.replace(".pdf", "")

        db.insert(
            "papers",
            {
                "id": paper_id,
                "user_id": user_id,
                "title": title,
                "file_url": file_url,
            },
        )

        db.insert(
            "reports",
            {
                "paper_id": paper_id,
                "report_text": summary_data.get("summary", ""),
                "pdf_url": report_url,
            },
        )

        return {
            "paper_id": paper_id,
            "title": title,
            "message": "Paper processed successfully",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    finally:
        if local_path.exists():
            local_path.unlink()


@router.get("/list")
async def list_papers(authorization: Optional[str] = Header(None)):
    """List all papers belonging to the authenticated user."""
    user_id = get_user_id(authorization)
    papers = db.select("papers", {"user_id": user_id})
    return {"papers": papers}


@router.get("/{paper_id}")
async def get_paper(paper_id: str, authorization: Optional[str] = Header(None)):
    """Get a single paper with its report."""
    user_id = get_user_id(authorization)
    paper = db.select_one("papers", {"id": paper_id, "user_id": user_id})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    report = db.select_one("reports", {"paper_id": paper_id})
    return {"paper": paper, "report": report}


@router.delete("/{paper_id}")
async def delete_paper(paper_id: str, authorization: Optional[str] = Header(None)):
    """
    Delete a paper and cascade-delete all associated data:
    report, quiz, flashcards, chat history, vector index, storage files.
    """
    user_id = get_user_id(authorization)
    paper = db.select_one("papers", {"id": paper_id, "user_id": user_id})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    # Delete storage files
    storage.delete_file(storage.PAPERS_BUCKET, f"{user_id}/{paper_id}.pdf")
    storage.delete_file(storage.REPORTS_BUCKET, f"{user_id}/{paper_id}_report.pdf")

    # Delete from DB (ON DELETE CASCADE handles child tables)
    db.delete_row("papers", {"id": paper_id})

    return {"message": "Paper and all associated data deleted successfully"}
