from services.groq_service import chat_completion


def summarize_paper(paper_data: dict) -> dict:
    """
    Summary Agent — generates a comprehensive, structured summary from paper data.

    Returns:
        {
            "title": str,
            "authors": [str],
            "keywords": [str],
            "summary": str   ← markdown-formatted multi-section summary
        }
    """
    sections_text = "\n\n".join(
        f"### {s['heading']}\n{s['content']}"
        for s in paper_data.get("sections", [])
        if s.get("content")
    )

    prompt = f"""You are a senior AI researcher. Write a comprehensive, insightful summary of this paper.

Paper Title: {paper_data.get("title", "Unknown")}
Authors: {", ".join(paper_data.get("authors", []))}
Abstract: {paper_data.get("abstract", "")}

Sections:
{sections_text[:8000]}

Write a structured summary using EXACTLY these section headings (use ## for each):

## Overview
Write 3–4 sentences explaining the paper's core contribution, novelty, and why it matters.

## Methodology
Explain the technical approach, model architecture, algorithms, or experimental design in detail.

## Results
Describe key findings, performance numbers, and what the results demonstrate.

## Benchmarks
List datasets used, baseline models compared against, and evaluation metrics.

## Limitations
Describe acknowledged limitations, edge cases the method doesn't handle, or future work needed.

## Key Takeaways
Provide 4–6 bullet points (using - ) of the most important insights a reader should remember.

Be specific, accurate, and use technical language appropriate for an AI/ML researcher audience."""

    summary = chat_completion(
        [
            {
                "role": "system",
                "content": (
                    "You are an expert academic researcher who writes clear, "
                    "precise, and insightful paper summaries for a technical audience."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=2048,
    )

    return {
        "title": paper_data.get("title", "Unknown"),
        "authors": paper_data.get("authors", []),
        "keywords": paper_data.get("keywords", []),
        "summary": summary,
    }
