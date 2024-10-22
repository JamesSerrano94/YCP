import json
import os
import re
from typing import List
from openai import OpenAI

system_prompt = f"""
You are an undergraduate academic advisor. You have access to a JSON dataset containing detailed information about various courses offered, including fields such as courseNumber, courseTitle, description, instructorList, meetingPattern, prerequisites, and distDesg (distribution designations).

Your task is to create a conflict-free schedule to users based on their interests and previous background. You must adhere to the following aspects to make a suitable schedule:

Prerequisites: Before you add a course, understand the course's prerequisites mentioned in description. Make sure the student is academically prepared based on the student's prior courses. If the course is too difficult for the student, recommend the prerequisite courses so that the student would be prepared in the long term.
Major: Consider the user's declared major to prioritize the major-required courses which they haven't taken yet. Visit this website for comprehensive details: https://catalog.yale.edu/ycps/subjects-of-instruction/computer-science/
Career Goals: Listen the user's stated career aspirations and gain domain knowledge on that field to suggest courses that align with their interests and goals. If the prerequisites of the user are not met, consider how to best prepare the student to take that course in the future
Distributional Designations: In your schedule, you must fulfill the number of distributional requirement courses which they have requested.

I want you to create the conflict-free schedule in an iterative way. Be aware of prerequisites mentioned in the course description. If the student's prior courses do not prepare them for the course you're about to recommend, do not recommend it. Instead recommend the prerequisites or other courses that will prepare them to succeed in that course. Firstly, choose courses that are required for their major which they haven't taken yet. Visit this website for comprehensive details on these major-required courses: https://catalog.yale.edu/ycps/subjects-of-instruction/computer-science/ Secondly, choose major-related (elective) courses that prepare them for their career goals or skills they're interested in learning. Thirdly, choose the number courses that fulfill the distributional requirements which they have requested. Make sure your schedule is conflict free.

Provide a brief explanation of how each recommended course relates to the user's major or career objectives.

Personalizing on the student's request, respond with a suitable schedule of 4-5 courses, providing relevant details:
- Subject Code: The subject code of the course
- Course Number: The course number
- Course Title: The name of the course
- Meeting Time: Meeting pattern of days of the week and times of day
- Distributional: The distributional requirement which is fulfilled
- Explanation: A brief, pedagogical explanation of how the course relates to the user's major or career objectives using relevant information from the course description. If the course does not directly relate to the student's career objectives right now, state how it prepares the student for more relevant courses. Be concise (less than 20 words).

Example Output:
1. 
- Subject Code: "CPSC"
- Course Number: "439"
- Course Title: "Software Engineering"
- Meeting Time: ['TTh 11.35-12.50']
- Distributional: "QR"
- Explanation: "You'll learn how to plan and design complex projects—essential for building machine learning models in production. Concepts like debugging, test-case generation, and static analysis will ensure your software is robust and scalable, which are critical in creating reliable ML pipelines. Additionally, the teamwork aspect mirrors real-world software development, preparing you for collaboration in machine learning-focused roles."

2. 
- Subject Code: "FILM"
- Course Number: "390"
- Course Title: "Media, AI and Algorithmic Bias "
- Meeting Time: ['TTh 11:35am-12:50pm']
- Distributional: "WR"
- Explanation: "By exploring real-world case studies like Netflix's recommendation system, you'll gain valuable skills in analyzing the ethical dimensions of AI, preparing you to design more responsible software systems."

You are not allowed to output anything else besides the required format. And your answer should strictly follow the example output format.
"""

def list_to_json(list_data: List[str], remove_embedding: bool = True, remove_cosine_similarity: bool = True) -> str:
    # Create a new list to store the modified dictionaries
    modified_list = []
    
    for item in list_data:
        # Create a copy of the dictionary to avoid modifying the original
        modified_item = item.copy()
        
        # Remove 'embedding' and 'cosine_similarity' keys from each dictionary in the list
        if remove_embedding and 'embedding' in modified_item:
            modified_item.pop('embedding')
        if remove_cosine_similarity and 'cosine_similarity' in modified_item:
            modified_item.pop('cosine_similarity')
        
        modified_list.append(modified_item)
    
    return json.dumps(modified_list)
        

class LLMRecommender:
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
        
    def get_course_recommendations(self, course_list: List[dict], major: str, career_goals: List[str], fulfilled_requirements: List[str]) -> List[str]:
        course_text = list_to_json(course_list)
        additional_info = f"Major: {major}\nCareer Goals: {career_goals}\nFulfilled Requirements: {fulfilled_requirements}"
        messages = [
            {"role": "system", "content": system_prompt.replace("_number_of_courses_to_recommend_for_llm", str(int(os.getenv('NUMBER_OF_COURSES_TO_RECOMMEND_FOR_LLM'))))},
            {"role": "assistant", "content": f"The JSON dataset of courses is as follows:\n{course_text}"},
            {"role": "user", "content": additional_info}
        ]
        
        # Call the OpenAI API to get the response
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Use "gpt-3.5-turbo" if you don't have access to GPT-4
                messages=messages,
                max_tokens=2000,
                n=1,
                stop=None,
                temperature=0.7,
            )

            # Extract the assistant's reply
            reply = response.choices[0].message.content.strip()
            recommended_course_list = self.parse_course_info(reply)
            
            # Put additional information for the recommended courses
            # TODO: Implement it with maybe dataframe to speed up the process
            for course in recommended_course_list:
                course_number = course["courseNumber"]
                other_course_info = next((item for item in course_list if item["courseNumber"] == course_number), None)
                if other_course_info is not None:
                    for key, value in other_course_info.items():
                        if key not in course:
                            course[key] = value
                
            
            return recommended_course_list

        except Exception as e:
            return f"An error occurred: {e}"
        
    def parse_course_info(self, text):
        # Split the text by course entries
        courses = re.split(r'\d+\.\s*\n', text)
        
        # List to store the parsed course information
        course_list = []

        # Regular expressions to match each field
        course_number_re = re.compile(r'- Course Number:\s*"(\d+)"')
        course_title_re = re.compile(r'- Course Title:\s*"([^"]+)"')
        explanation_re = re.compile(r'- Explanation:\s*"([^"]+)"')

        for course in courses:
            if course.strip():  # Skip any empty entries
                # Extract course number, title, and explanation using regex
                course_number = course_number_re.search(course)
                course_title = course_title_re.search(course)
                explanation = explanation_re.search(course)

                # Add to the course_list as a dictionary
                course_dict = {
                    "courseNumber": course_number.group(1) if course_number else None,
                    "courseTitle": course_title.group(1) if course_title else None,
                    "explanation": explanation.group(1) if explanation else None,
                }
                course_list.append(course_dict)

        return course_list
        
    
