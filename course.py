import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load configuration from .env file
load_dotenv()

class CanvasCourseManager:
    def __init__(self, api_url, api_token, account_id):
        self.api_url = api_url
        self.headers = {"Authorization": f"Bearer {api_token}"}
        self.account_id = account_id

    def create_course(self, course_name, course_code, start_date):
        course_data = {
            "course": {
                "name": course_name,
                "course_code": course_code,
                "start_at": start_date,
                "license": "private"
            }
        }
        response = requests.post(
            f"{self.api_url}/accounts/{self.account_id}/courses",
            headers=self.headers,
            json=course_data
        )
        return response.json()

    def create_modules(self, course_id, module_names):
        module_ids = []
        for module_name in module_names:
            response = requests.post(
                f"{self.api_url}/courses/{course_id}/modules",
                headers=self.headers,
                json={"name": module_name}
            )
            module_ids.append(response.json()["id"])
        return module_ids

    def create_assignments(self, course_id, assignments):
        for assignment in assignments:
            response = requests.post(
                f"{self.api_url}/courses/{course_id}/assignments",
                headers=self.headers,
                json={"assignment": assignment}
            )
            print(response.json())

    def create_quizzes(self, course_id, quizzes):
        for quiz in quizzes:
            response = requests.post(
                f"{self.api_url}/courses/{course_id}/quizzes",
                headers=self.headers,
                json={"quiz": quiz}
            )
            print(response.json())

    def configure_module_release_dates(self, course_id, module_ids, start_date, interval_weeks):
        release_dates = [
            start_date + timedelta(weeks=i) for i in range(len(module_ids))
        ]
        for module_id, unlock_date in zip(module_ids, release_dates):
            response = requests.put(
                f"{self.api_url}/courses/{course_id}/modules/{module_id}",
                headers=self.headers,
                json={"module": {"unlock_at": unlock_date.isoformat() + "Z"}}
            )
            print(response.json())

# Example usage:
if __name__ == "__main__":
    # Configuration from .env file
    API_URL = os.getenv("API_URL")
    API_TOKEN = os.getenv("API_TOKEN")
    ACCOUNT_ID = os.getenv("ACCOUNT_ID")
    
    # Initialize the manager
    manager = CanvasCourseManager(API_URL, API_TOKEN, ACCOUNT_ID)
    
    # Create the course
    course = manager.create_course(
        course_name="Foundation of Data Analysis",
        course_code="FDA101",
        start_date="2024-12-01T00:00:00Z"
    )
    course_id = course["id"]
    
    # Define module names
    modules = [
        "Introduction to Data Analysis",
        "Data Wrangling and Cleaning",
        "Data Visualization"
    ]
    
    # Create modules
    module_ids = manager.create_modules(course_id, modules)
    
    # Define assignments
    assignments = [
        {"name": "Basics of Data Analysis", "points_possible": 100},
        {"name": "Data Wrangling Assignment", "points_possible": 100},
        {"name": "Visualization Assignment", "points_possible": 100}
    ]
    
    # Create assignments
    manager.create_assignments(course_id, assignments)
    
    # Define quizzes
    quizzes = [
        {"title": "Data Analysis Fundamentals Quiz"},
        {"title": "Data Wrangling Quiz"},
        {"title": "Data Visualization Quiz"}
    ]
    
    # Create quizzes
    manager.create_quizzes(course_id, quizzes)
    
    # Configure module release dates
    start_date = datetime(2024, 12, 1)  # Start date for the first module
    manager.configure_module_release_dates(course_id, module_ids, start_date, interval_weeks=1)
