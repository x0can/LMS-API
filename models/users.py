import requests

class CanvasUserManager:
    def __init__(self, username, email, role, account_id, headers, api_url,api_token):
        self.account_id = account_id
        self.username = username
        self.email = email
        self.role = role  # 'instructor' or 'student'
        self.headers = headers
        self.api_url = api_url
        self.api_token = api_token

    def has_permission(self, action):
        
        
        """Check if the user has the permission to perform the given action"""
        permissions = {
            'instructor': ['create_course', 'edit_course', 'add_module', 'add_assignment', 'add_quiz', 'view_course', 'grade_assignments'],
            'student': ['view_course', 'submit_assignment', 'take_quiz']
        }

        return action in permissions.get(self.role, [])
 
        
    def _check_permissions(self, action):    
        if not self.has_permission(action):
            raise PermissionError(f"User '{self.username}' does not have permission to perform the action: {action}")
        

   
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
                return {"error": f"Course with ID {course_id} not found."}, 404
            # If some other error occurs, raise an exception
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while fetching course: {e}")
            return {"error": str(e)}, 500

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
                else:
                    print(f"Failed to enroll user {user_id}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while enrolling user: {e}")    
            
            
            
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
        
    # Function to fetch enrolled users in a course
    def fetch_enrolled_users(self,course_id):
        
        try:
        
            response = requests.get(f"{self.api_url}/courses/{course_id}/enrollments", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch enrollments for course {course_id}: {response.status_code}")
                return []   
            
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500            
                 