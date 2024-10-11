from openai import OpenAI
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
import Levenshtein

client = OpenAI(
    api_key='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'
)
# Define the path to your JSON file
file_path = 'C:\Yale\CS439\yale_courses_keywords.json'  # Replace with your actual file path

# Open and load the JSON file
with open(file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

prompt = "I want to become a software engineer focused on backend development. My goal is to develop scalable applications for financial institutions using cutting-edge cloud technologies."
prompt = "I'm passionate about AI and want to build conversational AI systems. I aim to work at a top AI lab like OpenAI or Google DeepMind"
prompt = "I aspire to be a data scientist working on predictive models for healthcare. I want to apply machine learning techniques to solve complex medical problems."
prompt = "I want to work as an investment banker focusing on mergers and acquisitions. My goal is to learn financial modeling and data analysis techniques to provide solutions for corporate clients."
prompt = "I want to create immersive virtual environments for educational platforms using VR technology."
prompt = "I want to become a novelist and literary critic. My goal is to analyze literature from different cultures and explore themes of identity and belonging in my writing."
prompt = "I am passionate about clinical psychology and mental health. My career goal is to work in psychotherapy and mental health services, focusing on cognitive behavioral therapy."
prompt = "I want to pursue a career in quantitative finance, specializing in risk management. My goal is to apply mathematical models to solve financial challenges."
prompt = "I aim to work in sports analytics, focusing on player performance prediction. My goal is to help teams optimize their strategies using data."


keywordsRequestGPT = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages = [
        {
            "role": "user",
            "content": "A student was prompted to give a description of courses they want to take this semester. Come up with keywords based on this prompt. Seperate them by comma. Do not use any other punctuation: " + prompt,
        }
    ],
    temperature=0.3, #convo needs to be boring
    max_tokens=256,
)

#print("KEYWORDS ARE: ", keywordsRequestGPT.choices[0].message.content)
keywordsRequest = keywordsRequestGPT.choices[0].message.content
keywordRequestArr = keywordsRequest.split(",")
print("Prompt is ", prompt)
for index, entry in enumerate(data):
    keywordsDB = entry['keywords'].split(",")
    maxRatio = 0
    for keyDB in keywordsDB:
        flag = False
        for userKey in keywordRequestArr:
            # print("USERKEY IS ", userKey)
            # print("keyDB IS ", keyDB)
            ratio = Levenshtein.distance(userKey, keyDB)
            # print("RATIO is ",ratio)
            # if ratio > maxRatio:
            #     maxRatio = ratio
            if ratio >= 27: #userKey.strip().lower() == keyDB.strip().lower():
                print("RECOMMENDED COURSE: ", entry['courseTitle'])
                flag = True
                break
        if flag:
            break





# for index, entry in enumerate(data):
#     string = entry['keywords'].split(',')
#     print("." + string[0].strip() + ".")
#     print()