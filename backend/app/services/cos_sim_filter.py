# app/services/cos_sim_filter.py

import os
import sys
from openai import OpenAI
import numpy as np
import re
import json

try:
    from app.configs.api_keys import APIKeysConfig
except ImportError:
    # If the import fails, adjust the sys.path to include the parent directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(current_dir))  # Goes up two levels
    sys.path.append(parent_dir)
    try:
        from app.configs.api_keys import APIKeysConfig
    except ImportError:
        # If still failing, report error
        raise ImportError("Cannot import APIKeysConfig")

class CosSimFilter:
    def __init__(self, openai_api_key=None):
        if openai_api_key:
            self.openai_client = OpenAI(api_key=openai_api_key)
        else:
            self.api_keys = APIKeysConfig()
            self.openai_client = OpenAI(api_key=self.api_keys.openai_api)

    def get_embedding(self, text):
        response = self.openai_client.embeddings.create(
            input=text,
            model='text-embedding-ada-002'
        )
        return response.data[0].embedding

    def process_course_data_as_dict_and_get_embedding(self, json_data):
        courses = []
        for course in json_data:
            course_info = {
                'courseNumber': course.get('courseNumber', ''),
                'courseTitle': course.get('courseTitle', ''),
                'description': course.get('description', ''),
                'instructorList': course.get('instructorList', []),
                'meetingPattern': course.get('meetingPattern', []),
            }

            course_text = f"{course_info['courseTitle']} {course_info['description']}"
            course_info['embedding'] = self.get_embedding(course_text)

            courses.append(course_info)
        return courses

    def cosine_similarity(self, a, b):
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def get_top_n_cos_sim_courses_given_user_input_and_json_data(self, user_input, json_data, n=5):
        user_input_embedding = self.get_embedding(user_input)

        courses = self.process_course_data_as_dict_and_get_embedding(json_data)

        for course in courses:
            course['cosine_similarity'] = self.cosine_similarity(user_input_embedding, course['embedding'])

        # print("courses: ", courses)
        top_n_courses = sorted(courses, key=lambda x: x['cosine_similarity'], reverse=True)[:n]

        return top_n_courses

# main to test
if __name__ == "__main__":
    test_json_file_dir = 'backend/app/services/example_yale_course_search_api_return.json'

    with open(test_json_file_dir, 'r') as f:
        json_data = json.load(f)

    cos_sim_filter = CosSimFilter()

    user_input = "What courses should I take if I want to be a game developer?"

    top_n_courses = cos_sim_filter.get_top_n_cos_sim_courses_given_user_input_and_json_data(user_input, json_data, n=5)

    for course in top_n_courses:
        print(course['courseNumber'], course['courseTitle'], course['cosine_similarity'])