from openai import OpenAI
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
import Levenshtein
import pathlib


def keywordSearch(prompt):
    client = OpenAI(
        api_key='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'
    )
    # Define the path to your JSON file
    curr_path = pathlib.Path(__file__).parent.absolute()
    print("current path: ", curr_path)
    file_path = str(curr_path) + '/yale_courses_keywords.json'  # Replace with your actual file path

    # Open and load the JSON file
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)


    keywordsRequestGPT = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [
            {
                "role": "user",
                "content": "A student was prompted to give a description of courses they want to take this semester. Come up with keywords based on the following prompt. Seperate them by comma. Do not use any other punctuation: " + prompt,
            }
        ],
        temperature=0.3, #convo needs to be boring
        max_tokens=256,
    )

    keywordsRequest = keywordsRequestGPT.choices[0].message.content
    keywordRequestArr = keywordsRequest.split(",")
    threshold = 27
    numCourses = 0
    recommendedCourses = []
    while numCourses == 0 and threshold > 0:
        for index, entry in enumerate(data):
            keywordsDB = entry['keywords'].split(",")
            for keyDB in keywordsDB:
                flag = False
                for userKey in keywordRequestArr:
                    ratio = Levenshtein.distance(userKey, keyDB)
                    if ratio >= threshold: 
                        recommendedCourses.append(entry)
                        numCourses += 1
                        flag = True
                        break
                if flag:
                    break
        threshold -= 1
        
    return recommendedCourses





# for index, entry in enumerate(data):
#     string = entry['keywords'].split(',')
#     print("." + string[0].strip() + ".")
#     print()