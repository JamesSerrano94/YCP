import requests
import json
import urllib.parse

API_KEY = "l71881101cd28e4091a40bc47b2808e0ef"
SUBJECT_API_URL = f"https://gw.its.yale.edu/soa-gateway/course/webservice/v2/subjects?apikey={API_KEY}"
COURSE_API_URL_TEMPLATE = "https://gw.its.yale.edu/soa-gateway/courses/webservice/v3/index?apikey={}&subjectCode={}&termCode={}"

# List of distributional designations to filter for
distributional_designations = [
    "YCHU", "YCL1", "YCL2", "YCL3", "YCL4", "YCL5", 
    "YCQR", "YCSC", "YCSO", "YCWR"
]

# Function to fetch all course codes
def fetch_course_codes():
    response = requests.get(SUBJECT_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch course codes: {response.status_code}")
        return []

# Function to fetch course details by subject code and term code
def fetch_course_details_by_subject_code(subject_code, term_code):
    subject_code = urllib.parse.quote(subject_code)
    print(subject_code)
    url = COURSE_API_URL_TEMPLATE.format(API_KEY, subject_code, term_code)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch courses for {subject_code} in term {term_code}: {response.status_code}")
        return []

# Function to check if a course has any of the required distributional designations
def has_distributional_designation(course):
    dist_desg = course.get("distDesg", [])
    return any(desg in distributional_designations for desg in dist_desg)

# Function to combine course data and save to a separate file for distributional courses
def combine_course_data_for_term(term_code, output_filename, dist_output_filename):
    combined_course_list = []
    distributional_course_list = []
    subject_codes = fetch_course_codes()
    print(subject_codes)
    
    for subject in subject_codes:
        subject_code = subject.get("code")
        if subject_code:
            print(f"Fetching courses for subject: {subject_code} in term {term_code}")
            course_details = fetch_course_details_by_subject_code(subject_code, term_code)
            
            if isinstance(course_details, list):
                for course in course_details:
                    # Check if required fields are present
                    if course.get("courseTitle") and course.get("department") and course.get("description"):
                        combined_course_list.append(course)
                        
                        # Check if the course has a required distributional designation
                        if has_distributional_designation(course):
                            distributional_course_list.append(course)
                    else:
                        print(f"Skipping course with missing data: {course.get('subjectNumber')}")
            else:
                print(f"Invalid response for subject {subject_code}: expected a list, got {type(course_details)}")
    
    # Save combined courses
    with open(output_filename, 'w') as outfile:
        json.dump(combined_course_list, outfile, indent=4)
    
    print(f"Combined course data saved to {output_filename}")
    
    # Save distributional courses
    with open(dist_output_filename, 'w') as dist_outfile:
        json.dump(distributional_course_list, dist_outfile, indent=4)
    
    print(f"Distributional course data saved to {dist_output_filename}")

if __name__ == "__main__":
    # Term codes for Fall 2024 and Spring 2025
    term_codes = {
        '202403': 'combined_course_data_fall_2024.json',
        '202501': 'combined_course_data_spring_2025.json'
    }
    
    for term_code, output_filename in term_codes.items():
        dist_output_filename = f"distributional_{output_filename}"
        print(f"Processing term {term_code}")
        combine_course_data_for_term(term_code, output_filename, dist_output_filename)
