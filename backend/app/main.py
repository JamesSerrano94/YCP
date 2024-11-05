"""
This module initializes the FastAPI app and includes the routers.
"""

from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
import os
from backend.app.routers import course
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# Set CORS origins dynamically
origins = [
    "http://localhost:3000",  # for local development
    os.getenv("PRODUCTION_URL")  # for production, should be set in your .env file
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(course.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)