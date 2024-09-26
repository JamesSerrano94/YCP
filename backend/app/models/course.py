# app/models/course.py

from pydantic import BaseModel
from typing import List, Optional

class Course(BaseModel):
    courseNumber: str
    courseTitle: str
    subjectCode: str
    subjectNumber: str
    description: str
    instructorList: List[str]
    meetingPattern: List[str]
    prerequisites: List[str]

class CourseRecommendationRequest(BaseModel):
    user_input: str