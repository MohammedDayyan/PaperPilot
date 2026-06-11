import json
import re
from services.pdf_service import extract_text_chunked
from services.groq_service import chat_completion


def read_paper(pdf_path: str) -> dict:
    """
    Reader Agent — extracts structured content from an academic PDF.

    Returns:
        {
            "title": str,
            "abstract": str,
            "authors": [str],
            "keywords": [str],
            "sections": [{"heading": str, "content": str}]
        }
    """
    raw_text = extract_text_chunked(pdf_path, max_chars=14000)

    prompt = f"""You are an expert academic paper reader. Carefully extract structured information from the paper below.

Return ONLY a single valid JSON object with this EXACT structure (no markdown, no extra text):
{{
  "title": "full paper title",
  "abstract": "complete abstract text",
  "authors": ["Author One", "Author Two"],
  "keywords": ["keyword1", "keyword2"],
  "sections": [
    {{
      "heading": "Introduction",
      "content": "section content here..."
    }}
  ]
}}

If a field cannot be found, use an empty string or empty array.

Paper text:
{raw_text}"""

    response = chat_completion(
        [
            {
                "role": "system",
                "content": (
                    "You extract structured data from academic papers. "
                    "Return ONLY valid JSON with no markdown code fences, no explanation."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=3000,
    )

    # Strip markdown fences if model wraps output
    response = response.strip()
    response = re.sub(r"^```(?:json)?", "", response).strip()
    response = re.sub(r"```$", "", response).strip()

    start = response.find("{")
    end = response.rfind("}") + 1
    if start == -1 or end == 0:
        return {
            "title": "Unknown Title",
            "abstract": "",
            "authors": [],
            "keywords": [],
            "sections": [],
        }

    return json.loads(response[start:end])
