# app/routers/course.py

from fastapi import APIRouter, HTTPException
from app.services.cos_sim_filter import CosSimFilter
from app.models.course import CourseRecommendationRequest
import os

router = APIRouter(
    prefix="/course",
    tags=["course"]
)

@router.post("/recommend")
async def recommend(request: CourseRecommendationRequest):
    # To test, use the following curl command:
    """
    curl -X POST "http://localhost:8000/course/recommend" \
    -H "Content-Type: application/json" \
    -d '{
      "major": "Computer Science",
      "semester": "Fall 2024",
      "schedulePreferences": {
        "earliestStartTime": "08:00 AM",
        "latestEndTime": "06:00 PM"
      },
      "careerGoals": "I want to be a game developer",
      "fulfilledRequirements": {
        "humanities": ["ENGL 114", "ENGL 120"],
        "sciences": ["CHEM 161", "CHEM 162"],
        "social": ["KREN L1 to L2"],
        "qr": ["MATH 120"],
        "writing": ["KREN L1 to L2"],
        "language": ["SPAN 110"],
        "priorCourses": ["MATH 225", "CPSC 201", "CPSC 323"]
      }
    }'
    """
    yale_course_search_api_key = os.getenv('YALE_COURSE_SEARCH_API_KEY')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    use_keyword_filtering = os.getenv('USE_KEYWORD_FILTERING')

    print("The received request is: ", request)
    print("yale_course_search_api_key: ", yale_course_search_api_key)
    print("openai_api_key: ", openai_api_key)
    print("use_keyword_filtering: ", use_keyword_filtering)

    # TODO: Step 1: Search based on front-end input, and exclude course that are already taken (Yang)

    # TODO: Step 2: Filter to reduce context length based to relevance of the careerGoals (the option is selected based on use_keyword_filtering(
    #       TODO: Option 1: Use cosine similarity on text embeddings (Xiatao)
    #       TODO: Option 2: Use keyword filtering (James)

    # TODO: Step 3: Parse into LLM for final output (Yangtian)

    # TODO: need to finalize the output for this POST request
    return {"llm_generated_text": "this is a placeholder for LLM generated text"}

