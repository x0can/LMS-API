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
                # Process the response to determine if permissions are granted
                permissions_info = response.json()
                if all(permissions_info.get(permission, False) for permission in permissions):
                    return True
                return False
            
            # Handle unexpected status codes
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to verify user permissions: {str(e)}")



    def create_course(self, name, start_at, license, course_code):
        
        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions to create a course.")
    
        
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
            raise Exception(f"Failed to create course: {str(e)}")


    def create_module(self, course_id, module_name):
        
        
        
        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions to create a module.")
    
        
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
            raise Exception(f"Failed to create module: {str(e)}")



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
            raise Exception(f"Failed to update module item: {str(e)}")





    def create_assignment(self, course_id, name, module_id):
        
        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions to create an assignment.")
    
        
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
                course_id, module_id, "Assignment", assignment['id'])
            return assignment
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create assignment: {str(e)}")



    def create_quiz(self, course_id, title, module_id):
        
        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions to create a quiz.")
    
        
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
                course_id, module_id, "Quiz", quiz['id'])
            return quiz
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create quiz: {str(e)}")


    def configure_module_release_dates(self, course_id, module_id, start_date, interval_weeks):
        
        
        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions to configure module release date.")
    
        
        """Set the release date for a module based on week intervals"""
        
        release_date = start_date + timedelta(weeks=interval_weeks)
        
        
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
            raise Exception(f"Failed to configure module release dates: {str(e)}")

    
