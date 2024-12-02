from datetime import timedelta
import requests


class CourseManager:
    def __init__(self, api_url, api_token, account_id, user):
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        self.account_id = account_id
        self.user = user
        
    def get_user_permissions(self, account_id, permissions):   
        try:
            # Prepare the data payload for permissions
            data = {f'permissions[]={permission}' for permission in permissions}

            # Fetch user permissions using Canvas API
            response = requests.post(
                f"{self.api_url}/accounts/{account_id}/permissions",
                headers=self.headers,
                data=data
            )
            
            if response.status_code == 200:
                return True
            else:
               return False, response.raise_for_status()
        except requests.exceptions.RequestException as e:
                return False

    def create_course(self, name, start_at, license, course_code):
        
        
        """Create a new course in Canvas."""
        course_data = {
            "course": {
                "name": name,
                "course_code": course_code,
                "start_at": start_at,
                "license": license
            }
        }
        try:
            response = requests.post(
                f"{self.api_url}/accounts/{self.account_id}/courses",
                headers=self.headers,
                json=course_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return None

    def create_module(self, course_id, module_name):
        
        
        """Create a module in the specified course."""
        module_data = {"name": module_name}
        try:
            response = requests.post(
                f"{self.api_url}/courses/{course_id}/modules",
                headers=self.headers,
                json=module_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return None


    def add_item_to_module(self, course_id, module_id, item_type, item_id):
        item_data = {
            "type": item_type,
            "content_id": item_id
        }
        try:
            response = requests.post(
                f"{self.api_url}/courses/{course_id}/modules/{module_id}/items",
                headers=self.headers,
                json=item_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return None




    def create_assignment(self, course_id, name, module_id):
        

        
        """Create an assignment and add it to a module."""
        assignment_data = {"name": name}
        try:
            response = requests.post(
                f"{self.api_url}/courses/{course_id}/assignments",
                headers=self.headers,
                json=assignment_data
            )
            response.raise_for_status()
            assignment = response.json()

            # Add the assignment to the module
            self.add_item_to_module(
                course_id, module_id, "assignments", assignment['id'])
            return assignment
        except requests.exceptions.RequestException as e:
            return None

    def create_quiz(self, course_id, title, module_id):
        
        
        """Create a quiz and add it to a module."""
        quiz_data = {"title": title}
        try:
            response = requests.post(
                f"{self.api_url}/courses/{course_id}/quizzes",
                headers=self.headers,
                json=quiz_data
            )
            response.raise_for_status()
            quiz = response.json()

            # Add the quiz to the module
            self.add_item_to_module(
                course_id, module_id, "quizzes", quiz['id'])
            return quiz
        except requests.exceptions.RequestException as e:
            return None

    def configure_module_release_dates(self, course_id, module_id, release_date):
        
        
        """Set the release date for a module."""
        module_data = {
            "unlock_at": release_date.isoformat()
        }
        try:
            response = requests.put(
                f"{self.api_url}/courses/{course_id}/modules/{module_id}",
                headers=self.headers,
                json=module_data
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            pass

    def configure_module_release_dates(self, course_id, module_ids, start_date, interval_weeks):
        """Set the release date for a module. based on interval of number of weeks"""

        release_dates = [
            start_date + timedelta(weeks=i * interval_weeks) for i in range(len(module_ids))
        ]
        try:
            for module_id, unlock_date in zip(module_ids, release_dates):

                module_data = {
                    "unlock_at": unlock_date.isoformat()
                }

                response = requests.put(
                    f"{self.api_url}/courses/{course_id}/modules/{module_id}",
                    headers=self.headers,
                    json=module_data
                )
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            pass
