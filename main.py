import os
from datetime import datetime
from canvas_course_manager import CanvasCourseManager

if __name__ == "__main__":
    
    # Configuration from .env file
    API_URL = os.getenv("API_URL")
    API_TOKEN = os.getenv("API_TOKEN")
    ACCOUNT_ID = os.getenv("ACCOUNT_ID")
    
    # Initialize the manager
    manager = CanvasCourseManager(API_URL, API_TOKEN, ACCOUNT_ID)
    
    # Create the course
    course = manager.create_course(
        course_name="Foundation of Data Analysis",
        course_code="FDA101",
        start_date="2024-12-01T00:00:00Z"
    )
    course_id = course["id"]
    
    # Define module names
    modules = [
        "Introduction to Data Analysis",
        "Data Wrangling and Cleaning",
        "Data Visualization"
    ]
    
    # Create modules
    module_ids = manager.create_modules(course_id, modules)
    
    # Define assignments
    assignments = [
        "Basics of Data Analysis",
        "Data Wrangling Assignment",
        "Visualization Assignment"
    ]
    
    # Create assignments
    manager.create_assignments(course_id, assignments)
    
    # Define quizzes
    quizzes = [
        {"title": "Data Analysis Fundamentals Quiz"},
        {"title": "Data Wrangling Quiz"},
        {"title": "Data Visualization Quiz"}
    ]
    
    # Create quizzes
    manager.create_quizzes(course_id, quizzes)
    
    # Configure module release dates
    start_date = datetime(2024, 12, 1)  # Start date for the first module
    manager.configure_module_release_dates(course_id, module_ids, start_date, interval_weeks=1)
    
    
    
    # call to fetch_user_progress
    USER_ID = 254  # Replace with your actual user ID
    user_progress = fetch_user_progress(COURSE_ID, USER_ID)
    if user_progress:
        print("User Progress:", user_progress)
