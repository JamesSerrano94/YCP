from fastapi import APIRouter, UploadFile, File, HTTPException
import PyPDF2
import io
import re

router = APIRouter(
    prefix="/transcript",
    tags=["transcript"]
)

@router.post("/upload")
async def upload_transcript(transcript: UploadFile = File(...)):
    try:
        # Verify file type
        if not transcript.content_type == "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Read the PDF content
        content = await transcript.read()
        pdf_file = io.BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Extract courses using regex
        # Updated pattern to match 2-4 letter department codes
        course_pattern = r'([A-Z]{2,4})\s*(\d{3})'
        matches = re.finditer(course_pattern, text)
        
        # Format courses and remove duplicates
        courses = [f"{match.group(1)} {match.group(2)}" for match in matches]
        unique_courses = list(set(courses))
        
        return {
            "courses": unique_courses,
            "message": "Transcript processed successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))