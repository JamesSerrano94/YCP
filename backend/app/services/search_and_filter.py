import json
import requests
import pandas as pd
import ast
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.models.course import CourseRecommendationRequest
from app.models.course import FulfilledRequirements
from app.models.course import SchedulePreferences
from app.configs.api_keys import APIKeysConfig

def retrive_desired_distributional(semester, humanity, science, social, quantitive, writing, language):
    '''
    Input: 
    semester: string - Fall 2024 OR Spring 2025
    others: boolean - whether or not to include this requirement in the returned json
    language: empty_string OR required_code("L1") OR required_code + speficy_language("L3 SPAN")
    returns: a json string
    '''
    semester_to_file = {
        # "Fall 2024": "distributional_combined_course_data_fall_2024.json",
        # "Spring 2025": "distributional_combined_course_data_spring_2025.json"
        "Fall 2024": "yale_courses_keywords_fall_2024.json",
        "Spring 2025": "yale_courses_keywords_spring_2025.json"
    }
    json_file_name = semester_to_file.get(semester)
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '../routers', json_file_name)
    file_path = os.path.abspath(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as json_file:
        datas = json.load(json_file)

    # print(data)
    lang_reqs = language.split()
    level = f"YC{lang_reqs[0]}" if len(lang_reqs) > 0 else None
    second_word = lang_reqs[1] if len(lang_reqs) > 0 else None
    result = []
    for data in datas:
        requirement = data.get("distDesg", [])
        if (humanity and 'YCHU' in requirement):
            # print(requirement)
            result.append(data)
        elif (science and 'YCSC' in requirement):
            result.append(data)
        elif (social and 'YCSO' in requirement):
            result.append(data)
        elif (quantitive and 'YCQR' in requirement):
            result.append(data)
        elif (writing and 'YCWR' in requirement):
            result.append(data)
        elif (level in requirement and second_word == data.get('subjectCode', '')):
            # print(data.get('courseTitle', ''))
            result.append(data)

    return result
    # return json.dumps(result)


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

# if __name__ == "__main__":
#    retrive_desired_distributional("Fall 2024", 0, 0, 0, 0, 0, "L3 SPAN")
# #    print(len(retrive_desired_distributional("Fall 2024", False, False, False, False, False, "L3 SPAN")))
