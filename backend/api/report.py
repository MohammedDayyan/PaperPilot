from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import Response
from typing import Optional

import services.supabase_service as db
import services.storage_service as storage
from api.deps import get_user_id

router = APIRouter()


@router.get("/{paper_id}")
async def get_report(paper_id: str, authorization: Optional[str] = Header(None)):
    """Get the report text for a paper."""
    user_id = get_user_id(authorization)

    paper = db.select_one("papers", {"id": paper_id, "user_id": user_id})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    report = db.select_one("reports", {"paper_id": paper_id})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return report


@router.get("/{paper_id}/download")
async def download_report(paper_id: str, authorization: Optional[str] = Header(None)):
    """Stream the report PDF as a file download."""
    user_id = get_user_id(authorization)

    paper = db.select_one("papers", {"id": paper_id, "user_id": user_id})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    report = db.select_one("reports", {"paper_id": paper_id})
    if not report or not report.get("pdf_url"):
        raise HTTPException(status_code=404, detail="Report PDF not available")

    try:
        pdf_bytes = storage.download_file(
            storage.REPORTS_BUCKET, f"{user_id}/{paper_id}_report.pdf"
        )
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="PaperPilot_Report_{paper_id[:8]}.pdf"'
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
