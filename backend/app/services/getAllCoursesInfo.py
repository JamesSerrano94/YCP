"""python script for fetching out all Yale offering courses, combine and save it to combined_course_data.json"""

import requests
import json

API_KEY = "l71881101cd28e4091a40bc47b2808e0ef"
SUBJECT_API_URL = f"https://gw.its.yale.edu/soa-gateway/course/webservice/v2/subjects?apikey={API_KEY}"
COURSE_API_URL_TEMPLATE = "https://gw.its.yale.edu/soa-gateway/courses/webservice/v3/index?apikey={}&subjectCode={}"

# Function to fetch all course codes
def fetch_course_codes():
    response = requests.get(SUBJECT_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch course codes: {response.status_code}")
        return []

# Function to fetch course details by subject code
def fetch_course_details_by_subject_code(subject_code):
    url = COURSE_API_URL_TEMPLATE.format(API_KEY, subject_code)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch courses for {subject_code}: {response.status_code}")
        return []

def combine_all_course_data():
    combined_course_list = []
    
    subject_codes = fetch_course_codes()
    
    for subject in subject_codes:
        subject_code = subject.get("code")
        if subject_code:
            print(f"Fetching courses for subject: {subject_code}")
            course_details = fetch_course_details_by_subject_code(subject_code)
            
            if isinstance(course_details, list):
                combined_course_list.extend(course_details)
            else:
                print(f"Invalid response for subject {subject_code}: expected a list, got {type(course_details)}")
    
    with open('combined_course_data.json', 'w') as outfile:
        json.dump(combined_course_list, outfile, indent=4)

    print("Combined course data saved to combined_course_data.json")

if __name__ == "__main__":
    combine_all_course_data()

