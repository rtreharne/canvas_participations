from canvasapi import Canvas
from config import *
import requests
from datetime import datetime
import tqdm
from tqdm import tqdm

def get_participations(course, enrollment):
    
    url = f"{CANVAS_API_URL}/api/v1/courses/{course.id}/analytics/users/{enrollment.user_id}/activity"
    headers = {
        "Authorization": f"Bearer {CANVAS_API_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        return None
    
def create_summary(course, enrollment):

    data_string = ""
    participations = get_participations(course, enrollment)
    if participations['page_views'] is None:
        return None
    else:
        for view in participations['page_views']:
            data_string += f"{enrollment.user['sortable_name']},{datetime.fromisoformat(view)},{participations['page_views'][view]}\n"
    
    return data_string

def get_assignments(course):
    assignments = [x for x in course.get_assignments() if x.published and x.has_submitted_submissions]
    return assignments

def get_assignment_submissions(assignment):
    submissions = [x for x in assignment.get_submissions(include=["user"]) if x.workflow_state == "graded"]
    return submissions

def build_assignment_dict(course, assignments):
    assignment_dict = {}
    for assignment in assignments:
        submissions = get_assignment_submissions(assignment)
        assignment_dict[assignment.name] = {x.user["sortable_name"]: x.score for x in submissions}

    return assignment_dict


def save_as_csv(fname, data_string):
    with open(fname, 'w') as f:
        f.write(data_string)

def main():
    print("Canvas Participation Report Generator, V1.0")
    print("")
    print("By R. Treharne, University of Liverpool, 2024")
    print("")

    # if there is a config file, use that
    try:
        from config import CANVAS_API_URL, CANVAS_API_TOKEN, course_id
        print("Using config.py file")
        print("")
        print("Canvas API URL: ", CANVAS_API_URL)
        print("Canvas API Token: ", CANVAS_API_TOKEN)   
        print("Course ID: ", course_id) 
    except:
        CANVAS_API_URL = input("Enter the Canvas API URL (e.g. https://canvas.liverpool.ac.uk): ")
        CANVAS_API_TOKEN = input("Enter the Canvas API Token: ")
        course_id = input("Enter the course ID: ")

    canvas = Canvas(CANVAS_API_URL, CANVAS_API_TOKEN)

    # Get the course object
    try:
        course = canvas.get_course(course_id)
    except:
        print("Course not found")
        exit()

    # Get the student enrollments
    print("")
    print("Getting student enrollments...")
    enrollments = [x for x in course.get_enrollments(include=["user"]) if x.type == "StudentEnrollment"]

    print("")
    print("Getting assignments...")
    assignments = get_assignments(course)
    
    fname = "output.csv"
    data_string = "last_name,first_name,datetime,page_views\n"

    print("")
    print("Generating report...")
    for enrollment in tqdm(enrollments[:]):
        data_string += create_summary(course, enrollment)

    print("")
    print("Saving report as output.csv")
    save_as_csv(fname, data_string)
    
if __name__ == "__main__":
    main()



