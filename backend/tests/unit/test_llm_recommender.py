from dotenv import load_dotenv
import pytest
from backend.app.services.llm_recommender import LLMRecommender
import os

@pytest.fixture
def test_courses():
    return [
        {
            "department": "CPSC",
            "courseTitle": "Introduction to Computing",
            "courseNumber": "100",
            "subjectNumber": "CPSC100",
            "meetingPattern": ["MW 9.00-10.15"],
            "description": "Introduction to computing concepts and programming",
            "distDesg": ["SC"]
        },
        {
            "department": "CPSC", 
            "courseTitle": "Data Structures",
            "courseNumber": "223",
            "subjectNumber": "CPSC223",
            "meetingPattern": ["TTh 10.30-11.45"],
            "description": "Data structures and algorithms",
            "distDesg": ["SC"]
        }
    ]

@pytest.fixture
def recommender(test_courses):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    return LLMRecommender(openai_api_key=api_key, course_list=test_courses)

def test_get_course_recommendations(recommender):
    """
    Test the course recommendations.
    """
    major = "Computer Science"
    career_goals = "Software Engineering"
    fulfilled_requirements = {"courses": ["CPSC 201"]}

    recommended_courses = recommender.get_course_recommendations(
        major,
        career_goals,
        fulfilled_requirements
    )

    assert isinstance(recommended_courses, list)
    assert len(recommended_courses) > 0

def test_recommend_non_conflicting_schedule(recommender):
    """
    Test the non-conflicting schedule recommendation.
    """
    schedule = recommender.recommend_non_conflicting_schedule()
    
    assert isinstance(schedule, list)
    assert len(schedule) > 0

    required_fields = ["department", "courseTitle", "courseNumber", "meetingPattern", "description"]
    for course in schedule:
        for field in required_fields:
            assert field in course, f"Field {field} missing from course"
            
            
def test_robust_output_in_llm_recommender(recommender):
    """
    Test the robustness of the LLM recommender by testing with a prefix and suffix.
    """
    llm_output_with_prefix_and_suffix = """
    Here are the courses that are most relevant to your major and career goals:
    1. 
    - Subject Number: "CPSC223"
    - Course Title: "Data Structures"
    - Meeting Time: "TTh 10.30-11.45"
    - Explanation: "Data Structures is a course that is directly related to a software engineer's role. It is a course that teaches you the basics of data structures and algorithms."
    
    2. 
    - Subject Number: "CPSC100"
    - Course Title: "Introduction to Computer Science"
    - Meeting Time: "MWF 10.30-11.20"
    - Explanation: "This is an introductory course in computer science that is directly related to a software engineer's role. It is a course that teaches you the basics of computer science and programming."
    Above are the courses that are most relevant to your major and career goals.
    """
    
    recommended_courses = recommender.parse_course_info(llm_output_with_prefix_and_suffix)
    assert isinstance(recommended_courses, list)
    assert len(recommended_courses) > 0

