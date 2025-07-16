from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
import io
import os
from pdf2image import convert_from_bytes
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # this is default on many systems
os.environ["TESSDATA_PREFIX"] = "./tessdata"  # 👈 tell it where to look
app = FastAPI()

# Enable CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Handle PDF
        if file.content_type == "application/pdf":
            try:
                images = convert_from_bytes(contents)
                all_text = ""
                for page in images:
                    text = pytesseract.image_to_string(page, lang="fas+eng")
                    all_text += text + "\n\n"
                return {"text": all_text.strip()}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

        # Handle image
        elif file.content_type.startswith("image/"):
            try:
                image = Image.open(io.BytesIO(contents))
                text = pytesseract.image_to_string(image, lang="fas+eng")
                return {"text": text.strip()}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")

        else:
            raise HTTPException(status_code=400, detail="File must be an image or PDF")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
