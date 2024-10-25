import json
import os
import re
from typing import List
from openai import OpenAI

from app.utils.exceptions import CourseNumberNotFoundError, LLMRecommenderError

system_prompt = f"""
You have access to a JSON dataset containing detailed information about various courses offered, including fields such as courseNumber, courseTitle, description, instructorList, meetingPattern, prerequisites, and distDesg (distribution designations).

Your task is to recommend courses to users based on their preferences. When a user asks for course recommendations, consider the following aspects to make suitable suggestions:

1. Course Level: Understand if the user prefers introductory (e.g., 100-level), intermediate (200-300-level), or advanced (400-level) courses.
2. Topics of Interest: Identify any keywords or topics mentioned by the user (e.g., "machine learning," "programming," "data science," "artificial intelligence") and find courses that match these topics in the courseTitle or description.
3. Instructor Preferences: If the user specifies an instructor, recommend courses taught by that instructor.
4. Schedule and Timing: Consider any mentioned schedule preferences, e.g., "afternoon classes," "MW"(which stands for Monday and Wednesday), "TTh" (Tuesday and Thursday), or specific times.
5. Prerequisites: Check if the user is looking for courses without prerequisites or if they meet the prerequisites based on their background.
6. Final Exam: If a user prefers courses without a final exam, filter accordingly.
7. Distribution Designations: Match courses that fulfill specific distribution designations if specified by the user (e.g., "Quantitative Reasoning," "Science").
8. Major: Consider the user's declared major or field of study to recommend relevant courses.
9. Career Goals: Take into account the user's stated career aspirations to suggest courses that align with their professional objectives.
10. Fulfilled Requirements: Be aware of the courses and requirements the user has already completed to avoid recommending redundant courses and to ensure progression in their academic journey.

When recommending courses, prioritize those that align with the user's major, support their career goals, and complement their existing academic achievements. Provide a brief explanation of how each recommended course relates to the user's major or career objectives.

Example Input from User:
- "I want to be a software engineer and I'm interested in machine learning."
- "I'm looking for an introductory course in computer science with no prerequisites."
- "Are there any advanced courses on machine learning that are offered on Tuesdays and Thursdays?"
- "I want to take a course taught by Professor Sohee Park."

Based on the user's request, respond with 2-3 suitable course options, providing relevant details:
- Course Number: The course code
- Course Title: The name of the course
- Explanation: A brief explanation of how the course relates to the user's major or career objectives

Example Output:
1. 
- Course Number: "439"
- Course Title: "Software Engineering"
- Explanation: "Software Engineering is a course that is directly related to a software engineer's role. It is a course that teaches you the basics of software engineering and how to build software."

2. 
- Course Number: "100"
- Course Title: "Introduction to Computer Science"
- Explanation: "This is an introductory course in computer science that is directly related to a software engineer's role. It is a course that teaches you the basics of computer science and programming."

If no exact matches are found, offer similar alternatives or suggest courses that are close to the user's requirements.

Now, given the JSON dataset and user preferences, recommend the most _number_of_courses_to_recommend_for_llm suitable courses.

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
                else:
                    raise CourseNumberNotFoundError(f"Course number {course_number} not found in the course list. "
                                                    f"First ensure that the given course list to llm is correct. "
                                                    f"Then, make sure that the course number is correct.")
                    
            # Check at least one course number is found
            if len(recommended_course_list) == 0:
                raise LLMRecommenderError("No course numbers found in the recommended course list. The input course list might be incorrect. Please try again.")
            
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
        
    
