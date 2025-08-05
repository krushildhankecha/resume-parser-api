import fitz  # PyMuPDF
import re
from .models import ResumeData

def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_resume(text: str) -> ResumeData:
    def extract(pattern, flags=0):
        match = re.search(pattern, text, flags)
        return match.group(0).strip() if match else None

    name = text.split('\n')[0].strip()  # crude name extraction

    return ResumeData(
        name=name,
        email=extract(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
        phone=extract(r"\+?\d[\d -]{8,}\d"),
        linkedin=extract(r"https?://(www\.)?linkedin\.com/in/[^\s]+"),
        github=extract(r"https?://(www\.)?github\.com/[^\s]+"),
        address=None,  # optional, advanced NLP needed
        skills=re.findall(r"(Python|Java|SQL|React|Node|C\+\+|AWS|Docker)", text, re.IGNORECASE),
        education=re.findall(r"(Bachelor|Master|B\.Tech|M\.Tech)[^.\n]*", text, re.IGNORECASE),
        experience=re.findall(r"(.*?)\n(?:\d{4}|\d+ years)", text),
        certifications=re.findall(r"(?i)certified[^.\n]*", text),
        projects=re.findall(r"(?i)project[^:\n]*:?.*?(?=\n|$)", text),
        summary=None  # optionally use LLM to generate
    )
