import json
import os
import re
from typing import List
from openai import OpenAI

from backend.app.utils.exceptions import CourseNumberNotFoundError, LLMRecommenderError

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

Based on the user's request, respond with _number_of_courses_to_recommend_for_llm suitable course options, providing relevant details:
- Subject Number: The subject number of the course
- Course Title: The name of the course
- Meeting Time: Meeting pattern of days of the week and times of day
- Explanation: A brief explanation of how the course relates to the user's major or career objectives

Example Output:
1. 
- Subject Number: "CPSC439"
- Course Title: "Software Engineering"
- Meeting Time: "TTh 11.35-12.50"
- Explanation: "Software Engineering is a course that is directly related to a software engineer's role. It is a course that teaches you the basics of software engineering and how to build software."

2. 
- Subject Number: "CPSC100"
- Course Title: "Introduction to Computer Science"
- Meeting Time: "MWF 10.30-11.20"
- Explanation: "This is an introductory course in computer science that is directly related to a software engineer's role. It is a course that teaches you the basics of computer science and programming."

If no exact matches are found, offer similar alternatives or suggest courses that are close to the user's requirements.

Now, given the JSON dataset and user preferences, recommend the most _number_of_courses_to_recommend_for_llm suitable courses.

You are not allowed to output anything else besides the required format. And your answer should strictly follow the example output format.
"""

schedule_prompt = f"""Please further find a non-conflicting schedule for the recommended classes. It should be a subset of the recommended courses and the meeting times should not overlap.

Example Output:
1. 
- Subject Number: "CPSC439"
- Course Title: "Software Engineering"
- Meeting Time: "TTh 11.35-12.50"
- Explanation: "Software Engineering is a course that is directly related to a software engineer's role. It is a course that teaches you the basics of software engineering and how to build software."

2. 
- Subject Number: "CPSC100"
- Course Title: "Introduction to Computer Science"
- Meeting Time: "MWF 10.30-11.20"
- Explanation: "This is an introductory course in computer science that is directly related to a software engineer's role. It is a course that teaches you the basics of computer science and programming."

Again, you should still directly output the same format as before, and you are not allowed to output anything else besides the required format. The output should be a list of courses with no conflicts in meeting times.
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
    def __init__(self, openai_api_key: str, course_list: List[dict]):
        self.client = OpenAI(api_key=openai_api_key)
        self.course_list = course_list  # Store the course list
        self.messages = []

        # Initialize the conversation
        course_text = list_to_json(course_list)
        self.messages = [
            {"role": "system", "content": system_prompt.replace("_number_of_courses_to_recommend_for_llm", str(int(os.getenv('NUMBER_OF_COURSES_TO_RECOMMEND_FOR_LLM'))))},
            {"role": "assistant", "content": f"The JSON dataset of courses is as follows:\n{course_text}"}
        ]

    def get_course_recommendations(self, major: str, career_goals: List[str], fulfilled_requirements: List[str]) -> List[dict]:
        additional_info = f"Major: {major}\nCareer Goals: {career_goals}\nFulfilled Requirements: {fulfilled_requirements}"
        # Append the user's message to the conversation
        self.messages.append({"role": "user", "content": additional_info})

        # Call the OpenAI API to get the response
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o", #  We can use gpt-4o-mini if we want to save money.
                messages=self.messages,
                max_tokens=2000,
                n=1,
                stop=None,
                temperature=0.7,
            )

            # Extract the assistant's reply
            reply = response.choices[0].message.content.strip()
            print(reply)
            # Append the assistant's message to the conversation
            self.messages.append({"role": "assistant", "content": reply})

            recommended_course_list = self.parse_course_info(reply)

            # Check that at least one course number is found
            if len(recommended_course_list) == 0:
                raise LLMRecommenderError("No course numbers found in the recommended course list. The input course list might be incorrect. Please try again.")

            return recommended_course_list

        except Exception as e:
            raise LLMRecommenderError(f"An error occurred in LLMRecommender: {e}")
        
    def recommend_non_conflicting_schedule(self) -> List[dict]:
        # Add schedule prompt to conversation
        self.messages.append({"role": "user", "content": schedule_prompt})

        MAX_RETRIES = int(os.getenv('MAX_RETRIES_FOR_LLM_RECOMMENDER'))
        try:
            for attempt in range(MAX_RETRIES):
                # Get LLM response
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=self.messages,
                    max_tokens=2000,
                    n=1,
                    stop=None,
                    temperature=0.7,
                )

                # Process response
                reply = response.choices[0].message.content.strip()
                self.messages.append({"role": "assistant", "content": reply})
                
                schedule = self.parse_course_info(reply)
                
                # Return if schedule is valid, otherwise retry
                if self.verify_non_conflicting_schedule(schedule):
                    return schedule
                    
                self.messages.append({
                    "role": "user", 
                    "content": "The recommended schedule is conflicting. Please try again."
                })

            raise LLMRecommenderError(
                "Unable to generate a non-conflicting schedule after maximum retries."
            )

        except Exception as e:
            raise LLMRecommenderError(f"An error occurred in LLMRecommender: {e}")

        
    def parse_course_info(self, text):
        # Split the text by course entries
        courses = re.split(r'\d+\.\s*\n', text)
        
        # List to store the parsed course information
        course_list = []

        # Regular expressions to match each field
        subject_number_re = re.compile(r'- Subject Number:\s*"([^"]+)"')
        course_title_re = re.compile(r'- Course Title:\s*"([^"]+)"')
        explanation_re = re.compile(r'- Explanation:\s*"([^"]+)"')
        meeting_time_re = re.compile(r'- Meeting Time:\s*"([^"]+)"')

        for course in courses:
            if course.strip():  # Skip any empty entries
                # Extract course number, title, and explanation using regex
                subject_number = subject_number_re.search(course)
                course_title = course_title_re.search(course)
                explanation = explanation_re.search(course)
                meeting_time = meeting_time_re.search(course)
                
                subject_number = subject_number.group(1) if subject_number else None
                course_title = course_title.group(1) if course_title else None
                explanation = explanation.group(1) if explanation else None
                meeting_time = meeting_time.group(1) if meeting_time else None
                
                # Add to the course_list as a dictionary
                course_dict = {
                    "subjectNumber": subject_number,
                    "courseTitle": course_title,
                    "explanation": explanation,
                    "meetingTime": meeting_time,
                }
                course_list.append(course_dict)
                
                other_course_info = next((item for item in self.course_list 
                                          if item["subjectNumber"] == subject_number), None)
                if other_course_info is not None:
                    for key, value in other_course_info.items():
                        if key not in course_dict:
                            course_dict[key] = value    
                else:
                    raise CourseNumberNotFoundError(f"Subject number {subject_number} not found in the course list. "
                                                    f"First ensure that the given course list to LLM is correct. "
                                                    f"Then, make sure that the subject number is correct.")

        return course_list
    

    def verify_non_conflicting_schedule(self, schedule: List[dict]):
        # Create a dictionary to store the time slots for each day
        time_slots = {day: [] for day in ['M', 'T', 'W', 'Th', 'F']}

        for course in schedule:
            meeting_pattern = course.get('meetingPattern', [])
            for pattern in meeting_pattern:
                # Extract day and time information
                match = re.match(r'([MTWThF]+)\s+(\d+\.\d+)-(\d+\.\d+)', pattern)
                if not match:
                    continue
                
                days, start_time, end_time = match.groups()
                
                # Convert time to minutes for easier comparison
                start_minutes = self.time_to_minutes(start_time)
                end_minutes = self.time_to_minutes(end_time)

                # Check for conflicts on each day
                day_list = []
                if 'Th' in days:
                    day_list.extend(['Th'])
                    days = days.replace('Th', '')
                day_list.extend(list(days))

                for day in day_list:
                    for existing_start, existing_end in time_slots[day]:
                        if (start_minutes < existing_end and end_minutes > existing_start):
                            return False  # Conflict found
                    
                    # If no conflict, add the time slot
                    time_slots[day].append((start_minutes, end_minutes))

        return True  # No conflicts found

    def time_to_minutes(self, time_str):
        # Convert time string to minutes (e.g., "13.30" to 810 minutes)
        hours, minutes = map(float, time_str.split('.'))
        return int(hours * 60 + minutes)
    
