# app/routers/course.py

import json
import time
import os
from typing import List
import pandas as pd
import ast
import requests
from fastapi import APIRouter, HTTPException, Depends
from backend.app.routers.cached_course_loader import load_cached_courses
from backend.app.services import search_and_filter
from backend.app.services.cos_sim_filter import CosSimFilter
from backend.app.models.course import CourseRecommendationRequest
from backend.app.models.course import FulfilledRequirements
from backend.app.models.course import SchedulePreferences
from backend.app.configs.api_keys import APIKeysConfig
from backend.app.services.llm_recommender import LLMRecommender
from backend.app.routers.login import require_auth
from backend.app.models.login import User
from dotenv import load_dotenv

router = APIRouter(
    prefix="/course",
    tags=["course"]
)

@router.post("/recommend")
async def recommend(request: CourseRecommendationRequest,
                    current_user: User = Depends(require_auth)):
    print("Current user is: ", current_user.net_id)
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
    }'
    """
    search_start_time = time.time()

    load_dotenv()
    yale_course_search_api_key = os.getenv('YALE_COURSE_SEARCH_API_KEY')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    use_cos_sim_filtering = os.getenv('USE_COS_SIM_FILTERING')
    number_of_courses_to_recommend = int(os.getenv('NUMBER_OF_COURSES_TO_RECOMMEND'))

    use_precomputed_embeddings = os.getenv('USE_PRECOMPUTED_EMBEDDINGS')

    print("The received request is: ", request)
    print("yale_course_search_api_key: ", yale_course_search_api_key)
    print("openai_api_key: ", openai_api_key)
    print("use_cos_sim_filtering: ", use_cos_sim_filtering)
    print("number_of_courses_to_recommend: ", number_of_courses_to_recommend)


    # Step 1: Search based on front-end input, and exclude course that are already taken (Yang)
    ## uncomment next line to run cpsc data only
    # data = search_course(request.semester, request.major)

    ## following are for all course data for a specific semester
    script_dir = os.path.dirname(os.path.abspath(__file__))
    semester_to_file = {
        "Fall 2024": "combined_course_data_fall_2024.json",
        "Spring 2025": "combined_course_data_spring_2025.json"
    }
    semester = request.semester if request.semester else None
    json_file_name = semester_to_file.get(semester)

    if json_file_name is None:
        raise ValueError(f"Unsupported semester: {request.semester}")

    # Construct the path to your JSON file
    json_file_path = os.path.join(script_dir, json_file_name)
    print(json_file_path)

    # Open and load the JSON file using the relative path
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    print("Search result from Yale Course Search API has department key: ", check_if_element_in_json_has_department_key(data))

    start_time = search_and_filter.convert_time_format(request.schedulePreferences.earliestStartTime)
    print(start_time)
    end_time = search_and_filter.convert_time_format(request.schedulePreferences.latestEndTime)
    print(end_time)
    taken_courses = search_and_filter.get_taken_courses(request.fulfilledRequirements)

    ###### Step 1 complete, df will be the filtered courses based on major, time, and taken courses ######
    #print("JSON after step 1 has department key: ", check_if_element_in_json_has_department_key(json.loads(output_json)))

    #Step 2: Filter to reduce context length based to relevance of the careerGoals

    loaded_cached_courses = load_cached_courses(request.semester)
    loaded_cached_courses = search_and_filter.filter_course_by_time(loaded_cached_courses, start_time, end_time, taken_courses)

    # This is a placeholder JSON when the search and keyworld filtering is not implemented
    # Need to replace this with actual search and keyword filtering
    # with open('app/services/example_yale_course_search_api_return.json', 'r') as f:
    #     loaded_cached_courses = json.load(f)
    # loaded_cached_courses = json.loads(output_json)
    # print(len(loaded_cached_courses))

    print("JSON after step 2.1 has department key: ", check_if_element_in_json_has_department_key(loaded_cached_courses))
    # Step 2.2: Use cosine similarity on text embeddings (Xiatao)
    cos_sim_start_time = time.time()
    cos_sim_filter = CosSimFilter(openai_api_key=openai_api_key, use_precomputed_embeddings=use_precomputed_embeddings)

    cos_sim_filtered_courses = cos_sim_filter.get_top_n_cos_sim_courses_given_user_input_and_json_data(request.careerGoals, 
                                                                                                       loaded_cached_courses,
                                                                                                       n=number_of_courses_to_recommend)

    print("Cosine similarity filtering took: ", time.time() - cos_sim_start_time)
    print("JSON after step 2.2 has department key: ", check_if_element_in_json_has_department_key(cos_sim_filtered_courses))

    distributional_courses = search_and_filter.retrive_desired_distributional(request.semester,
                                                                              request.needDistributionals.humanities,
                                                                              request.needDistributionals.sciences,
                                                                              request.needDistributionals.social,
                                                                              request.needDistributionals.qr,
                                                                              request.needDistributionals.writing,
                                                                              request.needDistributionals.language)
    distributional_courses = search_and_filter.filter_course_by_time(distributional_courses, start_time, end_time, taken_courses)
    distributional_cos_sim_filtered_courses = cos_sim_filter.get_top_n_cos_sim_courses_given_user_input_and_json_data(request.careerGoals, 
                                                                                                       distributional_courses, 
                                                                                                       n=number_of_courses_to_recommend)
    # Step 3: Parse into LLM for final output (Yangtian)
    # Transform cos_sim_filtered_courses into a JSON string

    # Initialize the LLM for final output
    llm = LLMRecommender(openai_api_key=openai_api_key, course_list=cos_sim_filtered_courses)
    distributional_llm = LLMRecommender(openai_api_key=openai_api_key, course_list=distributional_cos_sim_filtered_courses, if_distributional=True)

    try:
        # Get LLM recommendations based on the filtered courses and user request
        llm_recommended_courses = llm.get_course_recommendations(
            request.major,
            request.careerGoals,
            request.fulfilledRequirements,
            request.needDistributionals
        )
        distributional_llm_recommended_courses = distributional_llm.get_course_recommendations(
            request.major,
            request.careerGoals,
            request.fulfilledRequirements,
            request.needDistributionals
        )
        print("check llm.get_course_recommendations")
        
        # LLM recommends a non-conflicting schedule
        llm_recommended_non_conflicting_schedule = llm.recommend_non_conflicting_schedule()
        print("check llm_recommended_non_conflicting_schedule")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
    
    print("JSON after step 3 has department key: ", 
          check_if_element_in_json_has_department_key(llm_recommended_non_conflicting_schedule) & check_if_element_in_json_has_department_key(llm_recommended_courses))

    # The returned JSON should be a dict of course title, course number, time, description, distDesg. Other fields need to be dropped
    llm_recommended_courses_with_reduced_fields = reduce_fields(llm_recommended_courses)
    llm_recommended_non_conflicting_schedule_with_reduced_fields = reduce_fields(llm_recommended_non_conflicting_schedule)
    distributional_llm_recommended_courses_with_reduced_fields = reduce_fields(distributional_llm_recommended_courses)
    print(llm_recommended_courses_with_reduced_fields)
    print(llm_recommended_non_conflicting_schedule_with_reduced_fields)
    print(distributional_llm_recommended_courses_with_reduced_fields)
    
    # Remove duplicate courses in the recommended courses
    llm_recommended_courses_with_reduced_fields = reduce_duplicate_courses(llm_recommended_courses_with_reduced_fields, llm_recommended_non_conflicting_schedule_with_reduced_fields)
    distributional_llm_recommended_courses_with_reduced_fields = reduce_duplicate_courses(distributional_llm_recommended_courses_with_reduced_fields, llm_recommended_courses_with_reduced_fields)
    print("Total time taken: ", time.time() - search_start_time)
    return llm_recommended_courses_with_reduced_fields, llm_recommended_non_conflicting_schedule_with_reduced_fields, distributional_llm_recommended_courses_with_reduced_fields

def check_if_element_in_json_has_department_key(json):
    for element in json:
        if 'department' not in element:
            return False
    return True

def reduce_fields(courses: List[dict]):
    """
    Given a list of courses, reduce the fields of each course to only include the required fields.
    """
    return [
            {
                "department": course.get("department", ""),
                "courseTitle": course.get("courseTitle", ""),  
                "courseNumber": course.get("courseNumber", ""),  
                "time": course.get("meetingPattern", []),  
                "description": course.get("description", ""), 
                "distDesg": course.get("distDesg", []),
                "explanation": course.get("explanation", "")
            }
            for course in courses
        ]
    
def reduce_duplicate_courses(courses_A: List[dict], courses_B: List[dict]):
    """
    Given two lists of courses, reduce the courses in courses_A to only include courses that are not in courses_B.
    
    Example:
    courses_A = [{'courseNumber': 'CPSC 110'}, {'courseNumber': 'CPSC 201'}]
    courses_B = [{'courseNumber': 'CPSC 110'}]
    reduce_duplicate_courses(courses_A, courses_B) will return [{'courseNumber': 'CPSC 201'}]
    """
    courses_A_set = set(course['courseNumber'] for course in courses_A)
    courses_B_set = set(course['courseNumber'] for course in courses_B)
    return [course for course in courses_A if course['courseNumber'] not in courses_B_set]

# schedule_preferences = SchedulePreferences(
#     earliestStartTime="08:00 AM",
#     latestEndTime="06:00 PM"
# )

# fulfilled_requirements = FulfilledRequirements(
#     humanities=["ENGL 114", "ENGL 120"],
#     sciences=["CHEM 161", "CHEM 162"],
#     social=["KREN L1 to L2"],
#     qr=["MATH 120"],
#     writing=["KREN L1 to L2"],
#     language=["SPAN 110"],
#     priorCourses=["MATH225", "CPSC201", "CPSC323", "CPSC110"]
# )

# # Now create the CourseRecommendationRequest instance
# course_recommendation_request = CourseRecommendationRequest(
#     major="Computer Science",
#     semester="Fall 2024",
#     schedulePreferences=schedule_preferences,
#     careerGoals="I want to be a game developer",
#     fulfilledRequirements=fulfilled_requirements
# )

# recommend(course_recommendation_request)
