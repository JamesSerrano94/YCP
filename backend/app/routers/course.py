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
from app.models.course import NeededDistributionals
from app.configs.api_keys import APIKeysConfig
from app.services.llm_recommender import LLMRecommender
from . import YaleCoursePlannerKeyWordSearch
import re
from dotenv import load_dotenv

router = APIRouter(
    prefix="/course",
    tags=["course"]
)

router = APIRouter(
    prefix="/course",
    tags=["course"]
)

# Function to handle course times
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
    # Load environment variables
    load_dotenv()
    yale_course_search_api_key = os.getenv('YALE_COURSE_SEARCH_API_KEY')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    number_of_courses_to_recommend = int(os.getenv('NUMBER_OF_COURSES_TO_RECOMMEND'))

    print("The received request is: ", request)
    
    # Load course data from JSON file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    semester_to_file = {
        "Fall 2024": "combined_course_data_fall_2024.json",
        "Spring 2025": "combined_course_data_spring_2025.json"
    }
    json_file_name = semester_to_file.get(request.semester)

    if not json_file_name:
        raise ValueError(f"Unsupported semester: {request.semester}")

    json_file_path = os.path.join(script_dir, json_file_name)

    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        print(json_file_path)
        data = json.load(json_file)

    df = pd.json_normalize(data)

    
    # Convert start and end times to comparable formats
    start_time = convert_time_format(request.schedulePreferences.earliestStartTime)
    end_time = convert_time_format(request.schedulePreferences.latestEndTime)
    taken_courses = get_taken_courses(request.fulfilledRequirements)

    ###### Step 1: Filter out courses already taken ######
    df_filtered  = df


    ###### Step 2: Apply keyword search and cosine similarity for major-related courses ######
    # Step 2.1: Apply keyword filtering for major-related courses
    keyword_filtered_courses = YaleCoursePlannerKeyWordSearch.keywordSearch(request.careerGoals)

    filtered_courses = []
    # Create a set of subjectCode and courseNumber tuples from taken_courses
    taken_courses_set = set([tuple(course.split()) for course in taken_courses])
    for suggestedCourse in keyword_filtered_courses:
        courseStartTime, courseEndTime = findTimes(suggestedCourse['meetingPattern'])
        
        # Check time constraints
        if courseStartTime < start_time or courseEndTime > end_time:
            continue
        
        # Check if the course has already been taken

        if (suggestedCourse['subjectCode'], suggestedCourse['courseNumber']) in taken_courses_set:
            continue
        
        # Add to filtered list if all criteria are met
        filtered_courses.append(suggestedCourse)



    print(f"Number of courses after keyword and time filtering for major: {len(filtered_courses)}")

    # Step 2.2: Apply cosine similarity for major-related courses
    cos_sim_start_time = time.time()

    cos_sim_filter = CosSimFilter(openai_api_key=openai_api_key)
    cos_sim_filtered_major_courses = cos_sim_filter.get_top_n_cos_sim_courses_given_user_input_and_json_data(
        request.careerGoals, filtered_courses, n=number_of_courses_to_recommend
    )

    print(f"Cosine similarity filtering for major-related courses took {time.time() - cos_sim_start_time} seconds")

    def meets_distributional_requirements(course, need_distributionals):
        """
        Check if the course fulfills any of the user's specified distributional requirements.
        Excludes handling of language courses, which are dealt with separately.
        """
        dist_desg = course.get("distDesg", [])

        if (need_distributionals.humanities and "YCHU" in dist_desg) or \
        (need_distributionals.sciences and "YCSC" in dist_desg) or \
        (need_distributionals.social and "YCSO" in dist_desg) or \
        (need_distributionals.qr and "YCQR" in dist_desg) or \
        (need_distributionals.writing and "YCWR" in dist_desg):
            return True
        return False
    

    def find_next_language_course(needed_language, all_courses):
        """
        Recommend the next language course based on the language requirement (e.g., "L3 KREN").
        This function will return courses that match the required distributional level (e.g., "YCL3") and department (e.g., "KREN").
        """

        # Extract the language level and department from the needed_language (e.g., "L3 KREN")
        try:
            level, department = needed_language.split()
            required_ycl_level = f"YCL{level[-1]}"  # Convert "L3" to "YCL3"
        except (ValueError, IndexError):
            print("DEBUG: Invalid language format in need_distributionals.language")
            return []

        # Filter courses that match the department and the required YCL level
        next_language_courses = [
            course for course in all_courses
            if course.get("subjectCode", "") == department and required_ycl_level in course.get("distDesg", [])
        ]


        # Debugging the filtered courses
        print(f"DEBUG: Found {len(next_language_courses)} courses for {department} with {required_ycl_level}")
        return next_language_courses


    # def find_next_language_course(prior_courses, all_courses):
    #     """
    #     Recommend the next language course based on the max YCL level from prior courses.
    #     For example, if a user has taken KREN 110 (YCL1) and KREN 120 (YCL2), recommend KREN 130 (YCL3).
    #     This function is only triggered if need_distributionals.language is true.
    #     """

    #     max_ycl_for_language = {}

    #     for prior_course in prior_courses:
    #         prior_course_parts = prior_course.split()
    #         department = prior_course_parts[0]
    #         course_number = prior_course_parts[1]
    #         for course in all_courses:
    #             if course.get("subjectCode", "").startswith(department) and course.get("courseNumber", "") == course_number:
    #                 print(f"DEBUG: Matching course found in all_courses: {course.get('courseNumber', '')} (Department: {department})")
                    
    #                 dist_desg = course.get("distDesg", [])
    #                 print(f"DEBUG: Distributional designations for {course.get('courseNumber', '')}: {dist_desg}")

    #                 ycl_level = get_ycl_level_from_desg(dist_desg)
    #                 print(f"DEBUG: YCL level for course {course.get('courseNumber', '')}: {ycl_level}")

    #                 if ycl_level:  # Only consider courses with YCL designations
    #                     current_max_ycl = max_ycl_for_language.get(department, 0)
    #                     max_ycl_for_language[department] = max(current_max_ycl, ycl_level)
    #                     print(f"DEBUG: Updated max YCL for {department}: {max_ycl_for_language[department]}")




    #     result =[]
    #     print(max_ycl_for_language)
    #     for department, level in max_ycl_for_language.items():
    #         for course in all_courses:
    #             if course.get("courseNumber", "").startswith(department) and get_next_ycl_level(level) in course.get("distDesg", []):
    #                 result.append(course)
    #     return result    

    # def get_ycl_level_from_desg(dist_desg):
    #     """
    #     Given the 'distDesg' list of a course, return the YCL level if found.
    #     """
    #     ycl_mapping = {"YCL1": 1, "YCL2": 2, "YCL3": 3, "YCL4": 4, "YCL5": 5}
    #     for desg in dist_desg:
    #         if desg in ycl_mapping:
    #             return ycl_mapping[desg]
    #     return 0  # Return 0 if no YCL designation is found



    # def get_next_ycl_level(current_ycl_level):
    #     """
    #     Given the current YCL level, return the next YCL level.
    #     For example, if current_ycl_level is 2 (YCL2), return "YCL3".
    #     """
    #     ycl_level_mapping = {1: "YCL2", 2: "YCL3", 3: "YCL4", 4: "YCL5", 5: "YCL5"}
    #     return ycl_level_mapping.get(current_ycl_level)



    ###### Step 3: Filter courses based on non-language distributional requirements ######
    filtered_distributional_courses = [
        course for course in df_filtered.to_dict(orient="records")
        if meets_distributional_requirements(course, request.needDistributionals)
    ]

    print(f"Number of courses fulfilling distributional requirements before keyword search: {len(filtered_distributional_courses)}")

    ###### Step 4: Apply keyword search and cosine similarity ######
    # Step 4.1: Apply keyword search for distributional courses
    #filtered_distributional_courses = YaleCoursePlannerKeyWordSearch.keywordSearch(request.careerGoals, filtered_distributional_courses)

    print(f"Number of distributional courses after keyword filtering: {len(filtered_distributional_courses)}")

    # Step 4.2: Apply cosine similarity for distributional courses
    cos_sim_start_time = time.time()

    cos_sim_filtered_distributional_courses = cos_sim_filter.get_top_n_cos_sim_courses_given_user_input_and_json_data(
        request.careerGoals, filtered_distributional_courses, n=number_of_courses_to_recommend
    )

    print(f"Cosine similarity filtering for distributional courses took {time.time() - cos_sim_start_time} seconds")


    ###### Step 5: Ensure language recommendation based on next YCL level if needed ######
    if request.needDistributionals.language:
        next_language_courses = find_next_language_course(request.needDistributionals.language, df_filtered.to_dict(orient="records"))
    else:
        next_language_courses = []  # No next-level language courses if not required


    ###### Step 6: Combine all courses (major + distributional + next-level language) ######
    combined_courses = cos_sim_filtered_major_courses + cos_sim_filtered_distributional_courses + next_language_courses


    # Remove duplicates from combined courses
    combined_courses = remove_duplicate_courses(combined_courses)

    ###### Step 6: Print and return results before sending to LLM ######
    for course in combined_courses:
        print(f"""
        Subject Code: {course.get('subjectCode', '')}
        Course Number: {course.get('courseNumber', '')}
        Course Title: {course.get('courseTitle', '')}
        Description: {course.get('description', '')}
        Meeting Time: {course.get('meetingPattern', [])}
        Distribution Designations: {course.get('distDesg', [])}
        """)

    return None

# Function to remove duplicate courses based on course number
def remove_duplicate_courses(courses):
    unique_courses = []
    seen_courses = set()
    for course in courses:
        course_number = course.get("crn", "")
        if course_number not in seen_courses:
            unique_courses.append(course)
            seen_courses.add(course_number)
    return unique_courses

def filter(df, startTime, endTime, taken_courses):
    # Filter based on time range
    result = df[df['meetingPattern'].apply(lambda x: is_time_in_range(x, startTime, endTime, False))]

    # Create a set of subjectCode and courseNumber tuples from taken_courses
    taken_courses_set = set([tuple(course.split()) for course in taken_courses])

    # Filter out courses that match both subjectCode (department) and courseNumber from the taken_courses_set
    result = result[~result.apply(lambda x: (x['subjectCode'], x['courseNumber']) in taken_courses_set, axis=1)]

    # Reset the index after filtering
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
    if set(schedule_list[0].split(' ')[0]).issubset(valid_days):
        select = 0
    elif len(schedule_list) > 1 and set(schedule_list[1].split(' ')[0]).issubset(valid_days):
        select = 1
    else:
        return default

    time_part = schedule_list[select].split(' ')[1].split('-')
    start_time_hr = int(time_part[0].split('.')[0].replace('p', ''))
    start_time_min = int(time_part[0].split('.')[1].replace('p', ''))
    end_time_hr = int(time_part[1].split('.')[0].replace('p', ''))
    end_time_min = int(time_part[1].split('.')[1].replace('p', ''))

    # Convert hours and minutes to 24-hour format
    if start_time_hr <= 6:  # Assume times like 4pm are written as 4
        start_time_hr += 12
    if end_time_hr <= 6:
        end_time_hr += 12

    start_time_total = start_time_hr * 60 + start_time_min
    end_time_total = end_time_hr * 60 + end_time_min

    # Compare directly with the integer `start_time` and `end_time`
    if start_time_total >= start_time and end_time_total <= end_time:
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


schedule_preferences = SchedulePreferences(
    earliestStartTime="08:00 AM",
    latestEndTime="06:00 PM"
)

fulfilled_requirements = FulfilledRequirements(

    priorCourses=["MATH 225", "CPSC 201", "CPSC 323", "CPSC 110", 
                  "AFAM 115", "AFAM 250", 
                  "CHEM 161", "CHEM 162", 
                  "ECON 110", "SOCY 151", 
                  "MATH 120", 
                  "ENGL 114", "ENGL 120", 
                  "KREN 110", "KREN 120"]
)

need_distributionals = NeededDistributionals(
    humanities = 0,
    sciences = 1,
    social =0,
    qr = 0,
    writing = 0,
    language = "L3 SPAN"
)

# Now create the CourseRecommendationRequest instance
course_recommendation_request = CourseRecommendationRequest(
    major="Computer Science",
    semester="Fall 2024",
    schedulePreferences=schedule_preferences,
    careerGoals="I want to be a game developer",
    fulfilledRequirements=fulfilled_requirements,
    needDistributionals=need_distributionals

)

# Run the async function using asyncio
import asyncio
asyncio.run(recommend(course_recommendation_request))

