import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    KeepTogether,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


# ── Colour palette ────────────────────────────────────────────────────────────
DARK_NAVY = colors.HexColor("#0f172a")
INDIGO = colors.HexColor("#4f46e5")
SLATE = colors.HexColor("#64748b")
LIGHT_SLATE = colors.HexColor("#94a3b8")
WHITE = colors.white
DIVIDER = colors.HexColor("#e2e8f0")


def _build_styles() -> dict:
    base = getSampleStyleSheet()

    return {
        "brand": ParagraphStyle(
            "Brand",
            parent=base["Normal"],
            fontSize=9,
            textColor=INDIGO,
            fontName="Helvetica-Bold",
            spaceAfter=2,
            alignment=TA_LEFT,
        ),
        "title": ParagraphStyle(
            "DocTitle",
            parent=base["Normal"],
            fontSize=24,
            textColor=DARK_NAVY,
            fontName="Helvetica-Bold",
            spaceAfter=8,
            leading=30,
            alignment=TA_LEFT,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=base["Normal"],
            fontSize=9,
            textColor=SLATE,
            fontName="Helvetica",
            spaceAfter=3,
        ),
        "heading": ParagraphStyle(
            "SectionHeading",
            parent=base["Normal"],
            fontSize=13,
            textColor=INDIGO,
            fontName="Helvetica-Bold",
            spaceBefore=18,
            spaceAfter=6,
            alignment=TA_LEFT,
        ),
        "body": ParagraphStyle(
            "BodyText",
            parent=base["Normal"],
            fontSize=10,
            textColor=DARK_NAVY,
            fontName="Helvetica",
            spaceAfter=5,
            leading=16,
            alignment=TA_JUSTIFY,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["Normal"],
            fontSize=10,
            textColor=DARK_NAVY,
            fontName="Helvetica",
            spaceAfter=4,
            leading=16,
            leftIndent=16,
            bulletIndent=4,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base["Normal"],
            fontSize=8,
            textColor=LIGHT_SLATE,
            fontName="Helvetica",
            alignment=TA_CENTER,
        ),
    }


def generate_report_pdf(summary_data: dict) -> bytes:
    """
    Report Agent — converts a summary_data dict into a styled A4 PDF.
    Returns the PDF as raw bytes.
    """
    buffer = io.BytesIO()
    styles = _build_styles()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2.2 * cm,
        leftMargin=2.2 * cm,
        topMargin=2 * cm,
        bottomMargin=2.5 * cm,
    )

    story = []

    # ── Header block ──────────────────────────────────────────────────────────
    story.append(Paragraph("✦ PaperPilot AI", styles["brand"]))
    story.append(
        Paragraph(summary_data.get("title", "Research Paper"), styles["title"])
    )

    authors = summary_data.get("authors", [])
    if authors:
        story.append(Paragraph(f"Authors: {', '.join(authors)}", styles["meta"]))

    keywords = summary_data.get("keywords", [])
    if keywords:
        story.append(Paragraph(f"Keywords: {', '.join(keywords)}", styles["meta"]))

    story.append(
        Paragraph(
            f"Report generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}",
            styles["meta"],
        )
    )
    story.append(Spacer(1, 6))
    story.append(
        HRFlowable(width="100%", thickness=2, color=INDIGO, spaceAfter=10)
    )

    # ── Summary body ──────────────────────────────────────────────────────────
    summary_text = summary_data.get("summary", "No summary generated.")

    for line in summary_text.split("\n"):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 4))
        elif line.startswith("## "):
            heading_text = line[3:].strip()
            story.append(
                KeepTogether(
                    [
                        Paragraph(heading_text, styles["heading"]),
                        HRFlowable(
                            width="100%",
                            thickness=0.5,
                            color=DIVIDER,
                            spaceAfter=4,
                        ),
                    ]
                )
            )
        elif line.startswith(("- ", "* ", "• ")):
            bullet_content = line[2:].strip()
            story.append(Paragraph(f"• &nbsp; {bullet_content}", styles["bullet"]))
        else:
            story.append(Paragraph(line, styles["body"]))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 24))
    story.append(HRFlowable(width="100%", thickness=0.5, color=DIVIDER))
    story.append(Spacer(1, 6))
    story.append(
        Paragraph(
            "Generated by PaperPilot AI &nbsp;·&nbsp; Academic Research Intelligence Platform",
            styles["footer"],
        )
    )

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
