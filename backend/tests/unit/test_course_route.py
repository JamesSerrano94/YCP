# test_course.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.app.main import app
from backend.app.models.course import CourseRecommendationRequest
from backend.app.routers.course import router
import os
import json

# Fixture for the TestClient
@pytest.fixture
def client():
    app.dependency_overrides = {}
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}

# Mock data loader function
def mock_load_cached_courses(semester):
    # Return a list of mock courses
    return [
        {
            "department": "CPSC",
            "courseTitle": "Introduction to Programming",
            "courseNumber": "CPSC 100",
            "description": "Learn programming.",
            "meetingPattern": [{"days": "MWF", "start": "09:00 AM", "end": "09:50 AM"}],
            "distDesg": ["QR"],
        },
        # Add more mock courses as needed
    ]

# Mock LLMRecommender
class MockLLMRecommender:
    def __init__(self, openai_api_key, course_list, if_distributional=False):
        self.course_list = course_list
        self.if_distributional = if_distributional

    def get_course_recommendations(self, major, career_goals, fulfilled_requirements, need_distributionals):
        # Return the course list as-is for testing
        return self.course_list

    def recommend_non_conflicting_schedule(self):
        # Return a subset of courses for the schedule
        return self.course_list[:1]

# Mock CosSimFilter
class MockCosSimFilter:
    def __init__(self, openai_api_key=None, use_precomputed_embeddings=None):
        pass

    def get_top_n_cos_sim_courses_given_user_input_and_json_data(self, user_input, course_data, n=5, user_input_is_embedding=False):
        # Return the first 'n' courses for testing
        return course_data[:n]

# Test function
def test_recommend_success(client):
    # Override dependencies
    app.dependency_overrides = {
        # 'require_auth': lambda: User(net_id='testuser'),  # Uncomment if authentication is required
        'backend.app.routers.course.get_data_loader': lambda: mock_load_cached_courses,
        'backend.app.routers.course.get_llm_recommender_factory': lambda: MockLLMRecommender,
        'backend.app.routers.course.get_cos_sim_filter_factory': lambda: MockCosSimFilter,
        'backend.app.routers.course.get_openai_api_key': lambda: 'test-api-key',
    }

    # Prepare the request data
    request_data = {
        "major": "Computer Science",
        "semester": "Fall 2024",
        "schedulePreferences": {
            "earliestStartTime": "08:00 AM",
            "latestEndTime": "06:00 PM"
        },
        "careerGoals": "I want to be a game developer",
        "fulfilledRequirements": {
            "priorCourses": ["MATH 225", "CPSC 201", "CPSC 323"]
        },
        "needDistributionals": {
            "humanities": 0,
            "sciences": 0,
            "social": 1,
            "qr": 0,
            "writing": 0,
            "language": "L3 SPAN"
        }
    }

    response = client.post("/course/recommend", json=request_data)
    assert response.status_code == 200
    data = response.json()

    # Check that the response contains the expected structure
    assert isinstance(data, list)

