# app/routers/course.py

from fastapi import APIRouter, HTTPException
from app.services.cos_sim_filter import CosSimFilter
from app.models.course import CourseRecommendationRequest
import json
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
    use_cos_sim_filtering = os.getenv('USE_COS_SIM_FILTERING')
    number_of_courses_to_recommend = int(os.getenv('NUMBER_OF_COURSES_TO_RECOMMEND'))

    print("The received request is: ", request)
    print("yale_course_search_api_key: ", yale_course_search_api_key)
    print("openai_api_key: ", openai_api_key)
    print("use_cos_sim_filtering: ", use_cos_sim_filtering)
    print("number_of_courses_to_recommend: ", number_of_courses_to_recommend)

    # TODO: Step 1: Search based on front-end input, and exclude course that are already taken (Yang)

    # TODO: Step 2: Filter to reduce context length based to relevance of the careerGoals

    # TODO: Step 2.1: Use keyword filtering (James) 

    # This is a placeholder JSON when the search and keyworld filtering is not implemented
    # Need to replace this with actual search and keyword filtering
    with open('app/services/example_yale_course_search_api_return.json', 'r') as f:
        keyword_filtered_courses = json.load(f)

    # TODO: Step 2.2: Use cosine similarity on text embeddings (Xiatao)
    cos_sim_filter = CosSimFilter(openai_api_key=openai_api_key)

    cos_sim_filtered_courses = cos_sim_filter.get_top_n_cos_sim_courses_given_user_input_and_json_data(request.careerGoals, 
                                                                                                       keyword_filtered_courses, 
                                                                                                       n=number_of_courses_to_recommend)


    # TODO: Step 3: Parse into LLM for final output (Yangtian)

    # This is a placeholder JSON when the LLM querying is not implemented
    llm_recommended_courses = cos_sim_filtered_courses

    # The returned JSON should be a dict of course title, course number, time, description, distDesg. Other fields need to be dropped
    # Check if all courses have distDesg field
    llm_recommended_courses_with_reduced_fields = []
    all_have_distDesg = all("distDesg" in course for course in llm_recommended_courses)

    print("all_have_distDesg: ", all_have_distDesg)
        
    llm_recommended_courses_with_reduced_fields = [
            {
                "courseTitle": course.get("courseTitle", ""),  
                "courseNumber": course.get("courseNumber", ""),  
                "time": course.get("meetingPattern", []),  
                "description": course.get("description", ""), 
                "distDesg": course.get("distDesg", [])  
            }
            for course in llm_recommended_courses
        ]
    return llm_recommended_courses_with_reduced_fields

