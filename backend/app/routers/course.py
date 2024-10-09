# app/routers/course.py

import json
import os
import pandas as pd
import ast
from fastapi import APIRouter, HTTPException
from app.services.cos_sim_filter import CosSimFilter
from app.models.course import CourseRecommendationRequest
from app.models.course import FulfilledRequirements
# from app.models.course import SchedulePreferences

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


    # Step 1: Search based on front-end input, and exclude course that are already taken (Yang)

    ###### change later to actual json input ######
    with open('app/services/example_yale_course_search_api_return.json', 'r') as file:
        data = json.load(file)
    ###### change later to actual json input ######
    df = pd.json_normalize(data)
    start_time = convert_time_format(request.schedulePreferences.earliestStartTime)
    end_time = convert_time_format(request.schedulePreferences.latestEndTime)
    major = convert_major_format(request.major)
    taken_courses = get_taken_courses(request.fulfilledRequirements)
    df = filter(df, major, start_time, end_time, taken_courses)

    ###### Step 1 complete, df will be the filtered courses based on major, time, and taken courses ######


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

def filter(df, major, startTime, endTime, taken_courses):
    result = df[df['department'] == major]
    result = result[result['meetingPattern'].apply(lambda x: is_time_in_range(x, startTime, endTime, False))]
    taken_courses_split = [course.split() for course in taken_courses]
    taken_courses_df = pd.DataFrame(taken_courses_split, columns=['department', 'courseNumber'])
    result = result[~result.set_index(['department', 'courseNumber']).index.isin(taken_courses_df.set_index(['department', 'courseNumber']).index)]
    result.reset_index(drop=True, inplace=True)
    return result

def get_taken_courses(courses: FulfilledRequirements):
    result = []
    result.extend(courses.humanities)
    result.extend(courses.sciences)
    result.extend(courses.social)
    result.extend(courses.qr)
    result.extend(courses.writing)
    result.extend(courses.language)
    result.extend(courses.priorCourses)
    return result
   

def convert_major_format(major):
    # Need to add all major conversion, or do it in frontend
    if (major == "Computer Science"):
      return 'CPSC'

def is_time_in_range(string_list, start_time, end_time, default):
    valid_days = set('MThWF')
    schedule_list = ast.literal_eval(str(string_list))

    if len(schedule_list) == 0:
      return default

    select = 0
    if (set(schedule_list[0].split(' ')[0]).issubset(valid_days)):
      select = 0
    elif (len(schedule_list) > 1 and set(schedule_list[1].split(' ')[0]).issubset(valid_days)):
      select = 1
    else:
      return default

    time_part = (schedule_list[select].split(' ')[1]).split('-')
    start_time_hr = int(time_part[0].split('.')[0])
    start_time_min = int(time_part[0].split('.')[1])
    end_time_hr = int(time_part[1].split('.')[0])
    end_time_min = int(time_part[1].split('.')[1])

    if (start_time_hr <= 6):
      start_time_hr += 12
    if (end_time_hr <= 6):
      end_time_hr += 12
    start_time_total = start_time_hr * 60 + start_time_min
    end_time_total = end_time_hr * 60 + end_time_min

    start_time_obj = int(start_time.split('.')[0]) * 60 + int(start_time.split('.')[1])
    end_time_obj = int(end_time.split('.')[0]) * 60 + int(end_time.split('.')[1])

    if (start_time_total >= start_time_obj and end_time_total <= end_time_obj):
      return True

    return default

def convert_time_format(time):
    """
      06:00 PM will be convert to 18.00
    """
    time_small, period = time.split()
    hours, minutes = time_small.split(':')
    if period == 'AM':
        if hours == '12':
            hours = '00'
    elif period == 'PM':
        if hours != '12':
            hours = str(int(hours) + 12)
    return str(hours) + '.' + str(minutes)
