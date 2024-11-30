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