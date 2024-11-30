from datetime import datetime, timedelta
import json
from models.modules import Module
import requests


class CourseManager:

    def __init__(self, api_url, api_token, account_id):
        self.courses = []

        # Initialize api credentials

        self.api_url = api_url
        self.headers = {"Authorization": f"Bearer {api_token}"}
        self.account_id = account_id

    def create_course(self, name, start_at, license, course_code):
        course = Course(name, start_at, license, course_code)

        # Send Course details to Canvas Via API
        try:
            response = requests.post(
                f"{self.api_url}/accounts/{self.account_id}/courses",
                headers=self.headers,
                json=course
            )
            if response.status_code == 200:
                self.courses.append(course)
                return response.json()

            else:
                # debugger
                print(f"Failed to create course: {response.text}")
                return {"error": response.text}, response.status_code

        except requests.exceptions.RequestException as e:
            print(f"Error occurred while creating the course: {e}")
            return {"error": str(e)}, 500


class Course:
    def __init__(self, name, start_at, license, course_code):
        self.name = name
        self.start_at = start_at
        self.course_code = course_code
        self.license = license
        self.modules = []

    def add_module(self, course_id, module_name):
        response = requests.post(
            f"{self.api_url}/courses/{course_id}/modules",
            headers=self.headers,
            json={"name": module_name}
        )

        self.modules.append(response.json())

        return self.modules

    def configure_module_release_dates(self, course_id, start_date, interval_weeks):

        release_dates = [
            start_date + timedelta(weeks=i * interval_weeks) for i in range(len(self.modules))
        ]

        for module, unlock_date in zip(self.modules, release_dates):
            module_id = module['id']
            response = requests.put(
                f"{self.api_url}/courses/{course_id}/modules/{module_id}",
                headers=self.headers,
                json={"module": {"unlock_at": unlock_date.isoformat() + "Z"}}
            )
            if response.status_code != 200:
                raise Exception(
                    f"Failed to update module {module_id}: {response.json}")

            module["unlock_at"] = unlock_date.isoformat() + "Z"

            print(response.json())

    # def to_dict(self):
    #     """Converts the course object to a dictionary"""
    #     return {
    #         'title': self.name,
    #         'start_date': self.start_at,  # Converting datetime to string
    #         # Convert modules to dict
    #         'modules': [module.to_dict() for module in self.modules]
    #     }

    # def __repr__(self):
    #     """Return a JSON-like string representation of the course object"""
    #     return json.dumps(self.to_dict(), indent=4)  # JSON string with indentation for readability
