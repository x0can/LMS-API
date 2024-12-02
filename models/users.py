import requests
from datetime import datetime, timedelta


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
