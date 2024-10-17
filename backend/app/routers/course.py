# app/routers/course.py

import json
import time
import os
import pandas as pd
import ast
import requests
from fastapi import APIRouter, HTTPException
from app.services.cos_sim_filter import CosSimFilter
from app.models.course import CourseRecommendationRequest
from app.models.course import FulfilledRequirements
from app.models.course import SchedulePreferences
from app.configs.api_keys import APIKeysConfig
from app.services.llm_recommender import LLMRecommender
from . import YaleCoursePlannerKeyWordSearch
import re
from dotenv import load_dotenv

router = APIRouter(
    prefix="/course",
    tags=["course"]
)

def findTimes(meetingPattern):
    try:
        time_only = re.search(r'\d{1,2}\.\d{2}-\d{1,2}\.\d{2}', meetingPattern[0]).group()
        time_only = time_only.split("-")
        start = time_only[0].split(".")
        end = time_only[1].split(".")
        if int(start[0]) < 9:
            start[0] = int(start[0]) + 12
        if int(end[0]) < 9:
            end[0] = int(end[0]) + 12
        
        return 60 * int(start[0]) + int(start[1]), 60 * int(end[0]) + int(end[1])
    except:
        return 0, 1400
def check_if_element_in_json_has_department_key(json):
    for element in json:
        if 'department' not in element:
            return False
    return True

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
    load_dotenv()
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

    # Open and load the JSON file using the relative path
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    print("Search result from Yale Course Search API has department key: ", check_if_element_in_json_has_department_key(data))
    df = pd.json_normalize(data)
    start_time = convert_time_format(request.schedulePreferences.earliestStartTime)
    print(start_time)
    end_time = convert_time_format(request.schedulePreferences.latestEndTime)
    print(end_time)
    taken_courses = get_taken_courses(request.fulfilledRequirements)
    #df = filter(df, start_time, end_time, taken_courses)
    #output_json = df.to_json(orient="records", lines=False)

    ###### Step 1 complete, df will be the filtered courses based on major, time, and taken courses ######
    #print("JSON after step 1 has department key: ", check_if_element_in_json_has_department_key(json.loads(output_json)))

    #Step 2: Filter to reduce context length based to relevance of the careerGoals

    keyword_filtered_courses = YaleCoursePlannerKeyWordSearch.keywordSearch(request.careerGoals, semeser=semester)


    #Step 2.1: Use keyword filtering (James)
    filtered_courses = []
    for suggestedCourse in keyword_filtered_courses:
        courseStartTime, courseEndTime = findTimes(suggestedCourse['meetingPattern'])
        
        # Check time constraints
        if courseStartTime < start_time or courseEndTime > end_time:
            continue
        
        # Check if the course has already been taken
        if suggestedCourse['subjectNumber'] in taken_courses:
            continue
        
        # Add to filtered list if all criteria are met
        filtered_courses.append(suggestedCourse)

    keyword_filtered_courses = filtered_courses



    # This is a placeholder JSON when the search and keyworld filtering is not implemented
    # Need to replace this with actual search and keyword filtering
    # with open('app/services/example_yale_course_search_api_return.json', 'r') as f:
    #     keyword_filtered_courses = json.load(f)
    # keyword_filtered_courses = json.loads(output_json)
    # print(len(keyword_filtered_courses))

    print("JSON after step 2.1 has department key: ", check_if_element_in_json_has_department_key(keyword_filtered_courses))
    # TODO: Step 2.2: Use cosine similarity on text embeddings (Xiatao)
    cos_sim_start_time = time.time()
    cos_sim_filter = CosSimFilter(openai_api_key=openai_api_key)

    cos_sim_filtered_courses = cos_sim_filter.get_top_n_cos_sim_courses_given_user_input_and_json_data(request.careerGoals, 
                                                                                                       keyword_filtered_courses, 
                                                                                                       n=number_of_courses_to_recommend)
    print("Cosine similarity filtering took: ", time.time() - cos_sim_start_time)
    print("JSON after step 2.2 has department key: ", check_if_element_in_json_has_department_key(cos_sim_filtered_courses))
    # TODO: Step 3: Parse into LLM for final output (Yangtian)
    # Transform cos_sim_filtered_courses into a JSON string

    # Initialize the LLM for final output
    llm = LLMRecommender(openai_api_key=openai_api_key)

    # Get LLM recommendations based on the filtered courses and user request
    try:
        llm_recommended_courses = llm.get_course_recommendations(
            cos_sim_filtered_courses,
            request.major,
            request.careerGoals,
            request.fulfilledRequirements
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    print("JSON after step 3 has department key: ", check_if_element_in_json_has_department_key(llm_recommended_courses))

    # The returned JSON should be a dict of course title, course number, time, description, distDesg. Other fields need to be dropped
    llm_recommended_courses_with_reduced_fields = [
            {
                "department": course.get("department", ""),
                "courseTitle": course.get("courseTitle", ""),  
                "courseNumber": course.get("courseNumber", ""),  
                "time": course.get("meetingPattern", []),  
                "description": course.get("description", ""), 
                "distDesg": course.get("distDesg", []),
                "explanation": course.get("explanation", "")
            }
            for course in llm_recommended_courses
        ]
    return llm_recommended_courses_with_reduced_fields

def filter(df, startTime, endTime, taken_courses):
    result = df
    # result = df[df['department'] == major]
    result = result[result['meetingPattern'].apply(lambda x: is_time_in_range(x, startTime, endTime, False))]
    taken_courses_split = [course.split(' ', 1) for course in taken_courses]
    # print(taken_courses_split)
    taken_courses_df = pd.DataFrame(taken_courses_split, columns=['department', 'courseNumber'])
    result = result[~result.set_index(['department', 'courseNumber']).index.isin(taken_courses_df.set_index(['department', 'courseNumber']).index)]
    result.reset_index(drop=True, inplace=True)
    return result

def search_course(semester, major):
    search_api = APIKeysConfig.yale_course_search_api
    headers = {
        'apikey': search_api,
        'Accept': 'application/json',
    }
    params = {
                    'termCode': get_term_code(semester),
                    'subjectCode': convert_major_format(major),
                }
    response = requests.get("https://gw.its.yale.edu/soa-gateway/courses/webservice/v3/index", headers=headers, params=params)
    return response.json()

def get_term_code(term_str):
    splitted = term_str.split()
    termcode = '01'
    if (splitted[0] == "Summer"):
        termcode = '02'
    elif(splitted[0] == "Fall"):
        termcode = '03'
    return splitted[1] + termcode  

def get_taken_courses(courses: FulfilledRequirements):
    result = []
    result.extend(courses.humanities)
    result.extend(courses.sciences)
    result.extend(courses.social)
    result.extend(courses.qr)
    result.extend(courses.writing)
    result.extend(courses.language)
    result.extend(courses.priorCourses)
    # print(result)
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
    ## uncomment these to run cpsc data
    # time_part = (schedule_list[select].split(' ')[1]).split('-')
    # start_time_hr = int(time_part[0].split('.')[0])
    # start_time_min = int(time_part[0].split('.')[1])
    # end_time_hr = int(time_part[1].split('.')[0])
    # end_time_min = int(time_part[1].split('.')[1])

    # following are for all course data
    time_part = (schedule_list[select].split(' ')[1]).split('-')
    start_time_hr = int(time_part[0].split('.')[0].replace('p',''))
    start_time_min = int(time_part[0].split('.')[1].replace('p',''))
    end_time_hr = int(time_part[1].split('.')[0].replace('p',''))
    end_time_min = int(time_part[1].split('.')[1].replace('p',''))


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
    return 60* int(hours) + int(minutes)


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

