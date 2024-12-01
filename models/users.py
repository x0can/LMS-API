import requests

class CanvasUserManager:
    def __init__(self, username, email, role, account_id):
        self.account_id = account_id
        self.username = username
        self.email = email
        self.role = role  # 'instructor' or 'student'

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


