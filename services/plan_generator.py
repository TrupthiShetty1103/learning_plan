import json
import re
from services.together_client import chat_completion

def generate_daywise_plan(skill: str, deadline: str):
    prompt = f"""
You are an AI tutor.

Generate a realistic daily learning plan for "{skill}" to be completed by {deadline}.

Each module should:
- Cover one core topic
- Include 2–3 learning resources (videos/articles) with estimated time

Return valid JSON only:
[
  {{
    "day": 1,
    "title": "Module 1: Topic Title",
    "topics": ["..."],
    "resources": [
      {{"title": "...", "estimated_time": "... mins"}}
    ]
  }},
  ...
]
No markdown, no explanation. Just JSON.
"""
    raw = chat_completion(prompt)
    cleaned = re.sub(r"^```json|```$", "", raw.strip(), flags=re.IGNORECASE)

    try:
        return json.loads(cleaned)
    except Exception as e:
        raise ValueError(f"Invalid JSON from LLM: {str(e)}\n\nRAW OUTPUT:\n{raw}")
def generate_updated_plan(skill, reason, current_plan):
    prompt = f"""
You are an AI tutor.

The user is learning "{skill}" and has requested a plan update for this reason:
"{reason}"

Here is their current plan:
{json.dumps(current_plan)}

Please suggest a revised plan addressing their concern.

Return JSON like this:
[
  {{
    "day": 1,
    "title": "...",
    "topics": ["..."],
    "resources": [
      {{"title": "...", "estimated_time": "..."}}
    ]
  }},
  ...
]
Only return JSON.
"""

    raw = chat_completion(prompt)
    cleaned = re.sub(r"^```json|```$", "", raw.strip(), flags=re.IGNORECASE)
    return json.loads(cleaned)
