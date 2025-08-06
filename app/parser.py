import fitz  # PyMuPDF
import docx
from typing import Optional

def extract_text_from_resume(file_obj, content_type: str) -> Optional[str]:
    try:
        file_obj.seek(0)  # Make sure you're at start
        print(f"📄 Extracting text from file with content type: {content_type}")
        if content_type == "application/pdf":
            pdf_bytes = file_obj.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = "\n".join([page.get_text() for page in doc])

        elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # ✅ Important: reset the stream before reading with docx
            file_obj.seek(0)
            doc = docx.Document(file_obj)
            text = "\n".join([para.text for para in doc.paragraphs])

        else:
            return None

        return text.strip()

    except Exception as e:
        print(f"❌ Error in extract_text_from_resume: {e}")
        return None
