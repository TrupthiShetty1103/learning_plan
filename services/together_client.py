import os
import together
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

if not api_key:
    raise EnvironmentError("TOGETHER_API_KEY not found in .env")

client = together.Together(api_key=api_key)

def chat_completion(prompt: str) -> str:
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=4000,
    )
    return response.choices[0].message.content.strip()
