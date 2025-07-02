import json
import re
from services.together_client import chat_completion

def generate_assessment(topic: str, num_questions: int = 10):
    prompt = f"""
You are an expert tutor.

Generate {num_questions} high-quality multiple-choice questions on the topic: "{topic}" only.

Each question must:
- Be clear and relevant
-No question outside topics.
- Have 4 options labeled A, B, C, D
- Include the correct answer (e.g., "B")
- Include a short explanation of the correct answer

Return only a valid JSON list:
[
  {{
    "question": "...",
    "options": {{
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    }},
    "correct_answer": "B",
    "explanation": "..."
  }},
  ...
]
No markdown, no explanation — just raw JSON.
"""

    raw = chat_completion(prompt)
    cleaned = re.sub(r"^```json|```$", "", raw.strip(), flags=re.IGNORECASE)

    try:
        return json.loads(cleaned)
    except Exception as e:
        raise ValueError(f"Invalid JSON from LLM: {str(e)}\n\nRAW OUTPUT:\n{raw}")
