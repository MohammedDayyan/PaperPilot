import json
from services.groq_service import chat_completion


def generate_quiz(report_text: str) -> list[dict]:
    """
    Quiz Agent — generates a multiple-choice quiz of exactly 5 questions from the report text.

    Returns:
        [
            {
                "question": str,
                "options": [str, str, str, str],
                "correct_answer": str,
                "explanation": str
            },
            ...
        ]
    """
    prompt = f"""You are an expert educator. Based on the following academic paper summary, generate a multiple-choice quiz of exactly 5 questions to test a student's deep comprehension of the paper.

Paper Summary:
{report_text}

Output the quiz as a JSON object containing a "questions" key, which holds an array of 5 question objects.
Each question object MUST contain:
1. "question": The question text.
2. "options": An array of exactly 4 choices/options.
3. "correct_answer": The exact string from the "options" array that is the correct answer.
4. "explanation": A clear 1-2 sentence explanation of why this answer is correct, referencing the methodology or findings.

Ensure the questions cover different aspects: core contribution, methodology, results, and limitations.
Your response MUST be a single, valid JSON object and nothing else. Do not include markdown formatting or backticks.
"""

    response = chat_completion(
        [
            {
                "role": "system",
                "content": "You are a helpful assistant that generates quizzes in JSON format. Always return a single JSON object."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        json_mode=True
    )

    try:
        data = json.loads(response)
        if "questions" in data:
            return data["questions"]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Invalid format: " + response)
    except Exception as e:
        raise ValueError(f"Failed to parse quiz response as JSON: {str(e)}\nResponse: {response}")
