from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import uuid
from .parser import extract_text  # Assuming extract_text is defined in parser.py
from .parser import extract_text_from_pdf
from .groq_client import call_groq_for_resume_structuring
import json

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        return JSONResponse(content={"error": "Only PDF and DOCX files are supported"}, status_code=400)

    file_id = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, file_id)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        text = extract_text(file_path)
        ai_response = call_groq_for_resume_structuring(text)

        try:
            parsed_response = json.loads(ai_response)
        except Exception:
            return JSONResponse(content={"error": "AI response not valid JSON", "raw": ai_response})

        return parsed_response
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

