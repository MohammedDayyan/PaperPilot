import json
from services.groq_service import chat_completion


def generate_flashcards(report_text: str) -> list[dict]:
    """
    Flashcards Agent — generates a list of 8-10 key term/concept flashcards from the report text.

    Returns:
        [
            {
                "front": "Term / Question",
                "back": "Definition / Answer"
            },
            ...
        ]
    """
    prompt = f"""You are an expert tutor. Based on the following academic paper summary, generate a list of exactly 8 to 10 key terms, core concepts, or critical methodologies as flashcards.

Paper Summary:
{report_text}

Output the flashcards as a JSON object containing a "cards" key, which holds an array of flashcard objects.
Each flashcard object MUST contain:
1. "front": The term, abbreviation, or specific question (e.g., "What dataset was used for evaluation?" or "Interpretable Object").
2. "back": The concise definition, explanation, or answer (e.g., "The GLUE benchmark, testing language understanding." or "Neurons or attention heads identified as active").

Keep the definitions clear, concise, and focused on helping a student memorize the key points.
Your response MUST be a single, valid JSON object and nothing else. Do not include markdown formatting or backticks.
"""

    response = chat_completion(
        [
            {
                "role": "system",
                "content": "You are a helpful assistant that generates study flashcards in JSON format. Always return a single JSON object."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        json_mode=True
    )

    try:
        data = json.loads(response)
        if "cards" in data:
            return data["cards"]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Invalid format: " + response)
    except Exception as e:
        raise ValueError(f"Failed to parse flashcard response as JSON: {str(e)}\nResponse: {response}")
