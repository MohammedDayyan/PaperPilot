from services.groq_service import chat_completion


def generate_study_advice(report_text: str) -> str:
    """
    Study Advice Agent — generates a detailed study guide/advice in Markdown from the report text.

    Returns:
        Markdown text.
    """
    prompt = f"""You are a senior academic advisor. Based on the following academic paper summary, generate a structured, comprehensive study guide to help students master the paper's material.

Paper Summary:
{report_text}

Your response must be formatted in Markdown and must include EXACTLY the following section headers (use ## for each):

## Core Concepts to Master
Identify the 3-4 key theoretical or technical concepts that are fundamental to this paper, explaining why they are critical.

## Prerequisites & Background
List the background knowledge, math, programming models, or papers a student should be familiar with to fully understand this work.

## Reading Strategy
Suggest a step-by-step reading roadmap (e.g., what to focus on first, what to skim, and what to analyze deeply).

## Discussion Questions
Provide 4-5 deep, thought-provoking questions suitable for a seminar or group study discussion about the paper's implications, methodology, or assumptions.

## Practical Exercises & Projects
Suggest 1-2 practical, hands-on exercises or small project ideas that a student could build or run to experiment with the concepts.

Be motivating, educational, and technically precise."""

    advice = chat_completion(
        [
            {
                "role": "system",
                "content": (
                    "You are an expert academic advisor who writes helpful, structured study guides "
                    "in Markdown for graduate students."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.6,
        max_tokens=2048,
    )

    return advice
