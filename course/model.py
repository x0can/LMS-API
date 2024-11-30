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