from db.course_operations_faker import (
    create_sample_enrollments, create_sample_grades, create_sample_students, create_sample_subjects)
from models.course_sql_operations import CourseOperations
from flask import Flask
from routes import configure_routes
from config import Config
from db.student_queries import get_student_performance


# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)




# Configure routes
configure_routes(app)

from db.connection import get_connection

@app.route("/api/v1/report", methods=["GET"])
def fetch_report():
    """Fetch and display the student performance report."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = get_student_performance()
        cursor.execute(query)
        results = cursor.fetchall()
        report = [
            {
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "grade_level": row["grade_level"],
                "subject_name": row["subject_name"],
                "grade": row["grade"],
            }
            for row in results
        ]
        return {"data": report}, 200
    finally:
        cursor.close()
        conn.close()


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
    app.run(debug=True)
