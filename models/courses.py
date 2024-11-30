from datetime import datetime, timedelta
import json
from models.modules import Module

class CourseManager:
    
    def __init__(self):
        self.courses = []

    def create_course(self, title, description):
        course = Course(title, description)
        
        self.courses.append(course)
        return course



class Course:
    def __init__(self, title, start_date):
        self.title = title
        self.start_date = start_date
        self.modules = []

    def add_module(self, module_title, release_date=None):
        
        # Adds a module to the course with a release date 1 week interval
        if not release_date:
            # Default to 1-week interval from the current date
            release_date = datetime.utcnow() + timedelta(weeks=1)
            
    
        module = Module(module_title, release_date)
        
        self.modules.append(module)
        return module    

    def to_dict(self):
        """Converts the course object to a dictionary"""
        return {
            'title': self.title,
            'start_date': self.start_date.isoformat(),  # Converting datetime to string
            'modules': [module.to_dict() for module in self.modules]  # Convert modules to dict
        }

    def __repr__(self):
            """Return a JSON-like string representation of the course object"""
            return json.dumps(self.to_dict(), indent=4)  # JSON string with indentation for readability
