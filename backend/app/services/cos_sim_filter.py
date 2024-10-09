"""Module for filtering courses based on cosine similarity."""

import json
import os
import sys

import numpy as np
from openai import OpenAI

try:
    from app.configs.api_keys import APIKeysConfig
except ImportError:
    # If the import fails, adjust the sys.path to include the parent directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(current_dir))  # Goes up two levels
    sys.path.append(parent_dir)
    try:
        from app.configs.api_keys import APIKeysConfig
    except ImportError as exc:
        # If still failing, report error
        raise ImportError("Cannot import APIKeysConfig") from exc


class CosSimFilter:
    """Class for filtering courses based on cosine similarity of embeddings."""

    def __init__(self, openai_api_key=None):
        if openai_api_key:
            self.openai_client = OpenAI(api_key=openai_api_key)
        else:
            self.api_keys = APIKeysConfig()
            self.openai_client = OpenAI(api_key=self.api_keys.openai_api)

    def get_embedding(self, text):
        """Get the embedding of the given text using OpenAI API."""
        response = self.openai_client.embeddings.create(
            input=text,
            model='text-embedding-ada-002'
        )
        return response.data[0].embedding

    def process_course_data_as_dict_and_get_embedding(self, course_data):
        """Process course data and compute embeddings for each course."""
        courses = []
        for course in course_data:
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
        """Compute the cosine similarity between two vectors."""
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def get_top_n_cos_sim_courses_given_user_input_and_json_data(self, 
                                                                 user_input, 
                                                                 course_data, 
                                                                 n=5):
        """Get top N courses similar to user input."""
        user_input_embedding = self.get_embedding(user_input)

        courses = self.process_course_data_as_dict_and_get_embedding(course_data)

        for course in courses:
            course['cosine_similarity'] = self.cosine_similarity(user_input_embedding, course['embedding'])

        top_n_courses = sorted(
            courses,
            key=lambda x: x['cosine_similarity'],
            reverse=True
        )[:n]

        return top_n_courses


def main():
    """Main function to test CosSimFilter."""
    test_json_file_dir = os.path.join(
        'backend', 'app', 'services', 'example_yale_course_search_api_return.json'
    )
    with open(test_json_file_dir, 'r', encoding='utf-8') as f:
        course_data = json.load(f)

    cos_sim_filter = CosSimFilter()
    user_query = "What courses should I take if I want to be a game developer?"

    top_n_courses = cos_sim_filter.get_top_n_cos_sim_courses_given_user_input_and_json_data(
        user_query, course_data, n=5
    )

    for course in top_n_courses:
        print(course['courseNumber'], course['courseTitle'], course['cosine_similarity'])



if __name__ == "__main__":
    main()