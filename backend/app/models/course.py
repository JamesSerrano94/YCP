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

class SchedulePreferences(BaseModel):
    earliestStartTime: str
    latestEndTime: str

class FulfilledRequirements(BaseModel):
    humanities: List[str]
    sciences: List[str]
    social: List[str]
    qr: List[str]
    writing: List[str]
    language: List[str]
    priorCourses: List[str]

class CourseRecommendationRequest(BaseModel):
    major: str
    semester: str
    schedulePreferences: SchedulePreferences
    careerGoals: str
    fulfilledRequirements: FulfilledRequirements
