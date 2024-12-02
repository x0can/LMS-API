import requests


class CanvasUserManager:
    def __init__(self, api_url, api_token, account_id):
        self.account_id = account_id
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }
        self.api_url = api_url

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

    def get_user_info(self, user_identifier):
        """Fetch user information by username or email."""
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
        """Create a new user in Canvas."""
        try:
            user_data = {"user": {"name": name, "pseudonym": {"unique_id": email}}}
            response = requests.post(
                f"{self.api_url}/accounts/{self.account_id}/users",
                headers=self.headers,
                json=user_data,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error creating user: {str(e)}")

    def enroll_user(self, course_id, user_identifiers, role="StudentEnrollment"):
        """Enroll users in a specific course."""
        try:
            if not self.get_course(course_id):
                raise Exception(f"Course with ID {course_id} not found.")

            for user_identifier in user_identifiers:
                user_info = self.get_user_info(user_identifier)
                if not user_info:
                    user_info = self.create_user(user_identifier, user_identifier)
                    if not user_info:
                        print(f"Failed to create user {user_identifier}. Skipping...")
                        continue

                user_id = user_info["id"]
                enrollment_data = {
                    "enrollment": {
                        "user_id": user_id,
                        "type": role,
                        "enrollment_state": "active",
                    }
                }
                response = requests.post(
                    f"{self.api_url}/courses/{course_id}/enrollments",
                    headers=self.headers,
                    json=enrollment_data,
                )
                response.raise_for_status()
                print(f"User {user_id} successfully enrolled in course {course_id}.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error enrolling user: {str(e)}")

    def fetch_user_progress(self, course_id, user_id):
        """Fetch progress of a specific user in a course."""
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
        try:
            response = requests.get(
                f"{self.api_url}/courses/{course_id}/enrollments", headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching enrolled users: {str(e)}")
