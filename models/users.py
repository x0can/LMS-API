class User:
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