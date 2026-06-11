from pydantic import BaseModel
from typing import Optional


class ReportResponse(BaseModel):
    id: str
    paper_id: str
    report_text: str
    pdf_url: Optional[str] = None
