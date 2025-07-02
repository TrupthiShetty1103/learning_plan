import json
import re
from services.together_client import chat_completion

def generate_feedback_only(skill, score, total):
    prompt = f"""
You are an AI tutor.

A student has completed a course on "{skill}" and scored {score}/{total} on the final quiz.

1. Give concise feedback: identify strengths and weaknesses based on the score.
2. Suggest a few (3–5) high-priority topics or concepts the student should revisit or practice more.

Return valid JSON in this format:
{{
  "feedback": "...",
  "suggested_topics": ["...", "...", "..."]
}}

Only return the JSON. No markdown, no extra text.
"""
    raw = chat_completion(prompt)
    cleaned = re.sub(r"^```json|```$", "", raw.strip(), flags=re.IGNORECASE)

    try:
        result = json.loads(cleaned)
        return result["feedback"], result.get("suggested_topics", [])
    except Exception as e:
        raise ValueError(f"Invalid feedback JSON: {str(e)}\n\nRAW:\n{raw}")
