# app/main.py

from fastapi import FastAPI
from app.routers import courses
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()