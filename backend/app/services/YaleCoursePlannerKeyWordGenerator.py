from openai import OpenAI
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
#import bigFive

# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)
#client = OpenAI()
client = OpenAI(
    api_key='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'
)
# Define the path to your JSON file
file_path = '/Users/jiayangbao/Desktop/f24-yale-career-pathway-planner/test.json'  # combine courses
new_file_path = '/Users/jiayangbao/Desktop/f24-yale-career-pathway-planner/yale_courses_keywords.json' #keyword output new db
# Open and load the JSON file
with open(file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

for index, entry in enumerate(data):
    description = entry.get('description')  # Use .get() to safely access 'description'
    
    if description:  # Only proceed if description is not None
        keywords = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
              {
                  "role": "user",
                  "content": "This is the description for a course. Come up with keywords that can describe this course. Do not use bullet points. Seperate them by comma: " + description,
              }
            ],
            temperature=0.3,  # Make the response concise and not too creative
            max_tokens=256,
        )
        # Add the keywords to the entry
        entry['keywords'] = keywords.choices[0].message.content
    else:
        # If there's no description, set 'keywords' to an empty string or appropriate value
        entry['keywords'] = ""

with open(new_file_path, 'w', encoding='utf-8') as new_json_file:
    json.dump(data, new_json_file, indent=4, ensure_ascii=False)


# Print out the entire content
# print("All course entries:")
# for entry in data:
#     print(json.dumps(entry, indent=4))  # Pretty print each entry

# Optionally, print specific parts of the first entry
# print("\nFirst course details:")
# first_entry = data[0]
# print(f"Course Number: {first_entry['courseNumber']}")
# print(f"Course Title: {first_entry['courseTitle']}")
# print(f"Description: {first_entry['description']}")

#TO DO! Go through every course. Ask ChatGPT to come up with keywords for every course description. 
# Then make dictionary with keyword as key and course title as value
#Save dictionary to txt file
#load dictionary
#input prompt to chatGPT
#Tell it to find keywords
#loads every course with keywords
#if None, use Xiotao's method


# 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

# cont = True #create infinite loop
# print("Welcome to Psychoanaylsis chatbot. Type 'Goodbye!' to exit")

# name = input("What is your name? ")

# text = "" #only users inputs for psych report

# totaltext = "" #create transcript of whole convo
# while cont:
#   userMessage = input("\nEnter: ")
#   if userMessage == "Goodbye!": #end convo when you see this typed
#     cont = False
#   text = text + userMessage
  
  # response = client.chat.completions.create(
  #   model="gpt-3.5-turbo",

  #   messages = [
  #     {
  #         "role": "user",
  #         "content": "You are a psychologist chatbot. The user asked you the following message. Please respond with a question to the user. Question should be about getting to know user's personality on a very deep level.\n\n Message from user: " +
  #          userMessage + "\n\n Chatbot's response: ",
  #     }
  #   ],
  #   temperature=0.3, #convo needs to be boring
  #   max_tokens=256,
    
  # )
#   print("\n")
#   print(response.choices[0].message.content)
#   print("\n")
#   totaltext = totaltext + "\n" + userMessage + "\n" + response.choices[0].message.content

# analysis = client.chat.completions.create(
#     model="gpt-3.5-turbo",

#     messages = [
#       {
#           "role": "user",
#           "content": "You are a chatbot. Your job is to take the following text and rate the user on a percentage on the following personality traits: Openness, Consciousnes, Extraversion, Agreeableness and Neuroticism. Give a detailed reason for why each catagory is the way it is \n" +
#            text + "\n\n Chatbot's response: ",
#       }
#     ],
#     temperature=0.3,
#     max_tokens=1000, #for a detailed response
    
#   )

# print("\nYour analysis is:\n")
# print(analysis.choices[0].message.content)

# # file_path = name + ".txt"
# # file_pathRecord = name + "Record.txt"

# # # Open the file in write mode and write the string
# # with open(file_path, 'w') as file:
# #     file.write(analysis.choices[0].message.content)

# # with open(file_pathRecord, 'w') as file:
# #     file.write(totaltext)