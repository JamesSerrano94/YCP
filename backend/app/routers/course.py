# app/routers/course.py

from fastapi import APIRouter, HTTPException
from app.services import recommendation  # Absolute import
from app.models.course import CourseRecommendationRequest
import os