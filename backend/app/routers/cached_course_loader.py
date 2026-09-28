import os
from os.path import join, dirname
from dotenv import load_dotenv
import json

import pathlib


def load_cached_courses(semester):


    # Define the path to your JSON file
    curr_path = pathlib.Path(__file__).parent.absolute()
    print("current path: ", curr_path)
    if semester == "Fall 2024":
        file_path = str(curr_path) + '/yale_courses_keywords_fall_2024.json'  # Replace with your actual file path
    else:
        file_path = str(curr_path) + '/yale_courses_keywords_spring_2025.json'

    # Open and load the JSON file
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    return data
