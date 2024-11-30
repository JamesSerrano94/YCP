from fastapi.testclient import TestClient
from backend.app.routers.transcript import router
from fastapi import FastAPI
import pytest
import os

# Create a test FastAPI app
app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_upload_transcript_success():
    # Use existing test file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    test_pdf_path = os.path.join(parent_dir, "data", "transcript_sample.pdf")
    
    # Open test file
    with open(test_pdf_path, "rb") as f:
        files = {"transcript": ("transcript_sample.pdf", f, "application/pdf")}
        response = client.post("/transcript/upload", files=files)
    
    assert response.status_code == 200
    assert "courses" in response.json()
    assert "message" in response.json()
    assert response.json()["message"] == "Transcript processed successfully"
    assert isinstance(response.json()["courses"], list)
    # You might want to add specific assertions about the courses found in your sample PDF
    # For example:
    # assert "MATH 101" in response.json()["courses"]

def test_upload_transcript_wrong_file_type():
    files = {"transcript": ("test.txt", b"test content", "text/plain")}
    response = client.post("/transcript/upload", files=files)
    
    assert response.status_code == 400 or response.status_code == 500

def test_upload_transcript_empty_file():
    files = {"transcript": ("empty.pdf", b"", "application/pdf")}
    response = client.post("/transcript/upload", files=files)
    
    assert response.status_code == 500