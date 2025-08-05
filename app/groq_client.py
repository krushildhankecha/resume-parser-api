import requests
import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Set this in your env or .env

def call_groq_for_resume_structuring(raw_text: str):
    prompt = f"""
You are an AI Resume Parser. Given the following resume text, extract structured JSON with these fields:
- name
- email
- phone
- linkedin
- github
- address
- skills (list)
- education (list)
- experience (list)
- certifications (list)
- projects (list)
- summary

If a field is missing, set it to null. Respond ONLY with the JSON object. Here's the resume text:

\"\"\"{raw_text}\"\"\"
    """

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-70b-8192",  # or whatever model you prefer
            "messages": [
                {"role": "system", "content": "You are a helpful resume parsing assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
    )

    return response.json()["choices"][0]["message"]["content"]
