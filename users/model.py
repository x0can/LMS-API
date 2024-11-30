import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
 
class CanvasUserManager:
    # Initialize the CanvasUserManager with API configuration.
    def __init__(self, api_url, api_token, account_id):
        self.api_url = api_url
        self.api_token = api_token
        self.account_id = account_id
        self.headers = {
            "Authorization": f"Bearer {api_token}"
        } 
        
        
    def get_user_info(self, user_identifier):
        try:
            # Fetch user details using Canvas API
            response = requests.get(
               f"{self.api_url}/accounts/{self.account_id}/users",
                headers=self.headers,
               params={"search_term": user_identifier}  # Username or email
                )
            if response.status_code == 200:
                users = response.json()
                return users[0] if users else {"error": "User not found"}, 404
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
                print(f"Error occurred while fetching user info: {e}")
                return None
            
    # Create a new user if they do not already exist
    def create_user(self, name, email):
        try:
            user_data = {
                "user": {
                    "name": name,
                    "pseudonym": {
                        "unique_id": email
                    }
                }
            }
            response = requests.post(
                f"{self.api_url}/accounts/{self.account_id}/users",
                headers=self.headers,
                json=user_data
            )
            if response.status_code == 200:
                return response.json()  # Return user data if creation is successful
            else:
                print(f"Failed to create user: {response.text}")
                return {"error": response.text}, response.status_code
            
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while creating user: {e}")
            return {"error": str(e)}, 500    
        
    # Enroll a user into a course 
    def enroll_user(self, course_id, user_identifiers, role="StudentEnrollment"):
        try:
            # Verify  the course
            course = self.get_course(course_id)
            if not course:
                print(f"Course {course_id} creation failed.")
                return

            # Verify user information
            for user_identifier in user_identifiers:
            # Verify user information
                user_info = self.get_user_info(user_identifier)
                if not user_info:
                    print(f"User {user_identifier} not found....")
                    
                    # You can comment out this part if you do not have authority to add new users
                    # If user doesn't exist, create them
                    user_info = self.create_user(user_identifier, user_identifier)
                    
                    # You can comment out this part if you do not have authority to add new users
                    if not user_info:
                        print(f"Failed to create user {user_identifier}. Skipping...")
                        continue

                user_id = user_info['id']  # Extract the user ID from the user info

                # Define enrollment data
                enrollment_data = {
                    "user_id": user_id,
                    "type": role,
                    "enrollment_state": "active"  # Enroll immediately
                }

                # Send the POST request to enroll the user
                response = requests.post(
                    f"{self.api_url}/courses/{course_id}/enrollments",
                    headers=self.headers,
                    data=enrollment_data
                )
                if response.status_code == 200:
                    print(f"User {user_id} successfully enrolled in course {course_id}.")
                    return {"message": f"User {user_id} successfully enrolled in course {course_id}."}
                else:
                    print(f"Failed to enroll user {user_id}: {response.text}")
                    return {"error": response.text}, response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while enrolling user: {e}")  
            return {"error": str(e)}, 500  
            
    # Function to fetch enrolled users in a course
    def fetch_enrolled_users(course_id):
        
        url = f"{BASE_URL}/courses/{course_id}/enrollments"
        try:
            response = requests.get(
                url,
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to fetch enrollments: {response.text}"}, response.status_code
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500
        
    def fetch_user_progress(self, course_id, user_id):
        try:
            response = requests.get(
                f"{self.api_url}/courses/{course_id}/users/{user_id}/progress",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to fetch progress: {response.text}"}, response.status_code
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500            
        
    # Function to generate the report
    def generate_progress_report(course_id):
        enrollments = fetch_enrolled_users(course_id)
        progress_data = []

        for enrollment in enrollments:
            user_id = enrollment['user_id']
            user_progress = fetch_user_progress(course_id, user_id)
            if user_progress:
                progress_data.append({
                    "user_id": user_id,
                    "requirement_count": user_progress.get("requirement_count", "N/A"),
                    "requirement_completed_count": user_progress.get("requirement_completed_count", "N/A"),
                    "next_requirement_url": user_progress.get("next_requirement_url", "N/A"),
                    "completed_at": user_progress.get("completed_at", "N/A")
                })

        # Write the report to a CSV file
        with open("course_progress_report.csv", "w", newline="") as csvfile:
            fieldnames = ["user_id", "requirement_count", "requirement_completed_count", "next_requirement_url", "completed_at"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(progress_data)

        print("Course progress report saved as 'course_progress_report.csv'")    
        
        return progress_data