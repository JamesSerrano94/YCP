# app/main.py

from fastapi import FastAPI
from app.routers import course
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.include_router(course.router)