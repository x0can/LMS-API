from datetime import timedelta, datetime
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
        Generates an OAuth2 token using the Canvas API.
        """

        if not self.code:
            return "Authorization code is missing. Please authorize first."

        # Define endpoint and payload
        endpoint = f"{self.api_url}/login/oauth2/token"
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.account_id,
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
            self.handle_token(access_token)

            return access_token
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error generating OAuth2 token {str(e)}")

    def handle_token(self, access_token):
        self.access_token = access_token
        return "Authorization Successfull"

    def get_user_permissions(self, account_id, permissions):
        """Check if the user has the specified permissions."""
        try:
            data = {f"permissions[]={permission}" for permission in permissions}
            response = requests.post(
                f"{self.api_url}/accounts/{account_id}/permissions",
                headers=self.headers,
                data=data,
            )
            response.raise_for_status()
            permissions_info = response.json()
            return all(permissions_info.get(permission, False) for permission in permissions)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to verify user permissions: {str(e)}")

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

    def get_user_info(self, user_identifier):
        """Fetch user information by username or email."""

        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions")

        try:
            response = requests.get(
                f"{self.api_url}/accounts/{self.account_id}/users",
                headers=self.headers,
                params={"search_term": user_identifier},
            )
            response.raise_for_status()
            users = response.json()
            return users[0] if users else None
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch user info: {str(e)}")

    def get_course(self, course_id):
        """Fetch details for a specific course."""

        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions")

        try:
            response = requests.get(
                f"{self.api_url}/courses/{course_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return {"error": f"Course with ID {course_id} not found."}, 404
            raise Exception(f"Error fetching course: {response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching course: {str(e)}")

    def create_user(self, name, email):

        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions")

        """Create a new user in Canvas."""
        try:
            user_data = {"user": {"name": name,
                                  "pseudonym": {"unique_id": email}}}
            response = requests.post(
                f"{self.api_url}/accounts/{self.account_id}/users",
                headers=self.headers,
                json=user_data,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error creating user: {str(e)}")

    def enroll_user(self, course_id, data, role="StudentEnrollment", start_at=None, end_at=None):

        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions")

        """Enroll users in a specific course."""
        try:
            if not self.get_course(course_id):
                raise Exception(f"Course with ID {course_id} not found.")

            # Extract the user identifier and possibly other user details
            user_identifier = data.get("user_identifier")
            if not user_identifier:
                raise Exception("User identifier is required.")

            # Get user info or create a new user
            user_info = self.get_user_info(user_identifier)
            if not user_info:
                user_info = self.create_user(user_identifier, user_identifier)
                if not user_info:
                    print(
                        f"Failed to create user {user_identifier}. Skipping...")
                    return

            user_id = user_info["id"]

            # Set default enrollment start time if not provided
            start_at = start_at or datetime.utcnow().isoformat()
            # Handle default end date if not provided
            end_at = end_at or datetime.utcnow().replace(
                year=datetime.utcnow().year + 1).isoformat()

            enrollment_data = {
                "enrollment": {
                    "user_id": user_id,
                    "type": role,
                    "start_at": start_at,
                    "end_at": end_at,
                    "enrollment_state": "active",
                }
            }

            # Send the enrollment request
            response = requests.post(
                f"{self.api_url}/courses/{course_id}/enrollments",
                headers=self.headers,
                json=enrollment_data,
            )
            response.raise_for_status()
            print(
                f"User {user_id} successfully enrolled in course {course_id}.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error enrolling user: {str(e)}")

    def fetch_user_progress(self, course_id, user_id):
        """Fetch progress of a specific user in a course."""

        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions")

        try:
            response = requests.get(
                f"{self.api_url}/courses/{course_id}/users/{user_id}/progress",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching user progress: {str(e)}")

    def fetch_enrolled_users(self, course_id):
        """Fetch all enrolled users in a course."""

        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions")

        try:
            response = requests.get(
                f"{self.api_url}/courses/{course_id}/enrollments", headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching enrolled users: {str(e)}")

    def generate_progress_report(self, course_id):
        """Generate a progress report for all users in a course."""

        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions")

        try:
            # Fetch all enrolled users in the course
            enrolled_users = self.fetch_enrolled_users(course_id)
            if not enrolled_users:
                return {"error": f"No enrolled users found for course {course_id}"}

            # Compile progress data
            progress_report = []
            for enrollment in enrolled_users:
                user_id = enrollment.get("user_id")
                if user_id:
                    progress = self.fetch_user_progress(course_id, user_id)
                    progress_report.append({
                        "user_id": user_id,
                        "progress": progress
                    })

            return {"course_id": course_id, "progress_report": progress_report}
        except Exception as e:
            raise Exception(f"Failed to generate progress report: {str(e)}")
