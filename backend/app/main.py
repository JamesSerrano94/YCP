"""
This module initializes the FastAPI app and includes the routers.
"""

from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
from backend.app.routers import course
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

#for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(course.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)