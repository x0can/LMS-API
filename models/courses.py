from datetime import timedelta
import requests


class CourseManager:
    def __init__(self, api_url, account_id, redirect_url, client_secret, code=None, access_token=None):
        self.api_url = api_url
        self.account_id = account_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url
        self.access_token = access_token
        self.code = code
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"

        }

    def handle_redirect_callback_code(self, code):
        self.code = code
        return code

    def authorize_aouth2(self):

        endpoint = f"{self.api_url}/login/oauth2/auth"
        try:
            # Construct the authorization URL
            auth_url = f"{endpoint}?client_id={self.account_id}&response_type=code&redirect_uri={self.redirect_url}"
            return auth_url

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error generating OAuth2 token {str(e)}")

    def get_oauth2_token(self):
        """
        Generates an OAuth2 token using the Formstack API.
        """

        if not self.code:
            return "Authorization code is missing. Please authorize first."

        # Define endpoint and payload
        endpoint = f"{self.api_url}/login/oauth2/token"
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_url,
            "code": self.code
        }

        try:
            # Send POST request to get the token
            response = requests.post(endpoint, data=payload)

            # Raise an error if the request failed
            response.raise_for_status()

            # Return the access token if successful
            token_data = response.json()
            access_token = token_data.get('access_token')
            self.access_token = access_token

            return self.access_token
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error generating OAuth2 token {str(e)}")

    def create_course(self, name, start_at, license, course_code):

        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception(
                "User does not have the required permissions to create a course.")

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
            raise Exception(
                "User does not have the required permissions to create a module.")

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
            raise Exception(
                "User does not have the required permissions to create an assignment.")

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
            raise Exception(
                "User does not have the required permissions to create a quiz.")

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
            raise Exception(
                "User does not have the required permissions to configure module release date.")

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
            raise Exception(
                f"Failed to configure module release dates: {str(e)}")
