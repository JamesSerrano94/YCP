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
    priorCourses: List[str]

class NeededDistributionals(BaseModel):
    humanities: int
    sciences: int
    social: int
    qr: int
    writing: int
    language: str

class CourseRecommendationRequest(BaseModel):
    major: str
    semester: str
    schedulePreferences: SchedulePreferences
    careerGoals: str
    fulfilledRequirements: FulfilledRequirements
    needDistributionals: NeededDistributionals
