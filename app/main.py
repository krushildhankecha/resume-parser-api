from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import uuid
from .parser import extract_text_from_pdf, parse_resume

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return JSONResponse(content={"error": "Only PDF supported"}, status_code=400)

    file_id = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(UPLOAD_DIR, file_id)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        text = extract_text_from_pdf(file_path)
        result = parse_resume(text)
        return result.dict()
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
