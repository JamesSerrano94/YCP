"""
This module initializes the FastAPI app and includes the routers.
"""

from fastapi import FastAPI
from dotenv import load_dotenv
from app.routers import course

load_dotenv()

app = FastAPI()

app.include_router(course.router)
