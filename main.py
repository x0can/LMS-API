from db.connection import get_connection
from db.course_operations_faker import (
    create_sample_enrollments, create_sample_grades, create_sample_students, create_sample_subjects)
from models.course_sql_operations import CourseOperations
from flask import Flask
from routes import configure_routes
from config import Config
from flask_cors import CORS
import os


# Initialize Flask app
app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

CORS(app)

# Configure routes
configure_routes(app)



if __name__ == "__main__":
    course_operations = CourseOperations()
    course_operations.create_tables()
    # course_operations.clean_up()

    print("Populating database with sample data...")

    create_sample_students(10)
    create_sample_subjects()
    create_sample_enrollments(10, 5)
    create_sample_grades(10, 5)

    print("Database with sample data created")

    course_operations.close()
    app.run( host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 5000)))
