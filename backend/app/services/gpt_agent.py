import json
from openai import OpenAI

# Replace this with your actual OpenAI API key
client = OpenAI(api_key='Your OpenAI API key')

# Load the JSON data from a file or a string
# For this example, we'll assume the JSON data is in a file called 'courses.json'
with open('./backend/app/services/example_yale_course_search_api_return.json', 'r') as file:
    course_data = json.load(file)

# The prompt crafted earlier
system_prompt = """
You have access to a JSON dataset containing detailed information about various courses offered, including fields such as courseNumber, courseTitle, description, instructorList, meetingPattern, prerequisites, and distDesg (distribution designations).

Your task is to recommend courses to users based on their preferences. When a user asks for course recommendations, consider the following aspects to make suitable suggestions:

1. Course Level: Understand if the user prefers introductory (e.g., 100-level), intermediate (200-300-level), or advanced (400-level) courses.
2. Topics of Interest: Identify any keywords or topics mentioned by the user (e.g., "machine learning," "programming," "data science," "artificial intelligence") and find courses that match these topics in the courseTitle or description.
3. Instructor Preferences: If the user specifies an instructor, recommend courses taught by that instructor.
4. Schedule and Timing: Consider any mentioned schedule preferences, e.g., "afternoon classes," "MW"(which stands for Monday and Wednesday), "TTh" (Tuesday and Thursday), or specific times.
5. Prerequisites: Check if the user is looking for courses without prerequisites or if they meet the prerequisites based on their background.
6. Final Exam: If a user prefers courses without a final exam, filter accordingly.
7. Distribution Designations: Match courses that fulfill specific distribution designations if specified by the user (e.g., "Quantitative Reasoning," "Science").

Example Input from User:
- "I'm looking for an introductory course in computer science with no prerequisites."
- "Are there any advanced courses on machine learning that are offered on Tuesdays and Thursdays?"
- "I want to take a course taught by Professor Sohee Park."

Example Output:

Based on the user's request, respond with 2-3 suitable course options, providing relevant details such as:
- Course Number: The course code
- Course Title: The name of the course
- Description: A brief description of the course content
- Instructor: Name(s) of the instructor(s)
- Schedule: The days and times the course meets
- Prerequisites: Any prerequisites required for the course
- Distribution Designations: Applicable designations (if any)

If no exact matches are found, offer similar alternatives or suggest courses that are close to the user's requirements.

Tips:
- If the user is open to suggestions, recommend popular or highly relevant courses from the dataset.
- Always clarify if you’re unsure about the user’s preferences by asking follow-up questions before providing recommendations.

Now, given the JSON dataset and user preferences, recommend the most suitable courses.
"""

# Function to generate recommendations based on user input
def get_course_recommendations(user_input):
    # Prepare the messages for the chat completion
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": f"The JSON dataset of courses is as follows:\n{json.dumps(course_data)}"},
        {"role": "user", "content": user_input}
    ]

    # Call the OpenAI API to get the response
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Use "gpt-3.5-turbo" if you don't have access to GPT-4
            messages=messages,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extract the assistant's reply
        reply = response.choices[0].message.content.strip()
        return reply

    except Exception as e:
        return f"An error occurred: {e}"

# Main interaction loop
def main():
    print("Welcome to the Course Recommender!")
    print("Please enter your preferences for course recommendations.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        recommendations = get_course_recommendations(user_input)
        print(f"\nAssistant:\n{recommendations}\n")

if __name__ == "__main__":
    main()
