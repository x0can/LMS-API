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
        
    #fetch course details
    def get_course(self, course_id):
            

        try:
            response = requests.get(
                f"{self.api_url}/courses/{course_id}",
                    headers=self.headers
            )
            # If course is found, return the course details
            if response.status_code == 200:
                return response.json()

            # If course is not found (404)
            elif response.status_code == 404:
                print(f"Course with ID {course_id} not found")
                   

                # If some other error occurs, raise an exception
            else:
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Error occurred while fetching course: {e}")
            return None
        
        
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
                    if users:
                        return users[0]  # Assuming the first user is the correct one
                    else:
                        print(f"No user found with identifier: {user_identifier}")
                        return None
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
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while creating user: {e}")
            return None    