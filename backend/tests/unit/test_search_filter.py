import pytest
import json
import io
from backend.app.services import search_and_filter
from backend.app.models.course import FulfilledRequirements

# Sample data for testing
sample_courses_data = [
    {
        "distDesg": ["YCHU", "YCSC", "YCQR"],
        "subjectCode": "SPAN",
        "meetingPattern": ["1.00-2.30", "3.00-4.30"],
        "subjectNumber": "101"
    },
    {
        "distDesg": ["YCSO", "YCWR"],
        "subjectCode": "FRCH",
        "meetingPattern": ["10.00-11.30", "2.00-3.30"],
        "subjectNumber": "102"
    }
]

@pytest.fixture
def fulfilled_requirements():
    return FulfilledRequirements(
        priorCourses=["MATH 225", "CPSC 201", "CPSC 323"]
    )

def test_retrive_desired_distributional(monkeypatch):
    def mock_open(*args, **kwargs):
        return io.StringIO(json.dumps(sample_courses_data))

    # Mock the open function to return sample data
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: mock_open())

    result = search_and_filter.retrive_desired_distributional(
        semester="Fall 2024",
        humanity=1,
        science=0,
        social=0,
        quantitive=1,
        writing=0,
        language="L1 SPAN"
    )
    assert len(result) > 0
    assert any("YCHU" in course['distDesg'] for course in result)
    assert any("YCQR" in course['distDesg'] for course in result)

def test_filter_course_by_time():
    courses = sample_courses_data
    usr_start_time = 60 * 10
    usr_end_time = 60 * 15 + 30
    taken_courses = ["101"]

    result = search_and_filter.filter_course_by_time(
        courses, usr_start_time, usr_end_time, taken_courses
    )
    assert len(result) == 1
    assert result[0]["subjectNumber"] == "102"

def test_convert_time_format():
    assert search_and_filter.convert_time_format("10:00 AM") == 600
    assert search_and_filter.convert_time_format("1:00 PM") == 780
    assert search_and_filter.convert_time_format("12:00 AM") == 0
    assert search_and_filter.convert_time_format("12:00 PM") == 720

def test_get_taken_courses(fulfilled_requirements):
    result = search_and_filter.get_taken_courses(fulfilled_requirements)
    assert "MATH225" in result
    assert "CPSC201" in result

def test_findTimes():
    meeting_pattern = ["1.00-2.30", "3.00-4.30"]
    usr_start_time = 60 * 13  # 1:00 PM in minutes
    usr_end_time = 60 * 17  # 5:00 PM in minutes

    assert search_and_filter.findTimes(meeting_pattern, usr_start_time, usr_end_time) == True

    meeting_pattern = ["1.00-2.30", "6.00-7.30p"]
    assert search_and_filter.findTimes(meeting_pattern, usr_start_time, usr_end_time) == False