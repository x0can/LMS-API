from flask import Blueprint
from db.connection import get_connection
from flasgger.utils import swag_from
from db.student_queries import get_student_performance


report_routes = Blueprint('report_routes', __name__)


@report_routes.route("/api/v1/report")
@swag_from({
    "tags": ["Student performance report"],
    'responses': {
        302: {
            'description': 'Fetch and display the student performance report.'
        }
    }
})
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
