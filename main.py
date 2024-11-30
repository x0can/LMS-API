from flask import Flask, jsonify, request
import os
from datetime import datetime
from dotenv import load_dotenv
from course.model import CanvasCourseManager

from users.model import CanvasUserManager

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize the CanvasCourseManager
API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

manager = CanvasCourseManager(API_URL, API_TOKEN, ACCOUNT_ID)
user_manager = CanvasUserManager(API_URL, API_TOKEN, ACCOUNT_ID)



@app.route('/api/create_course', methods=['POST'])
def create_course():
    
    data = request.json
    course_name = data.get("course_name")
    course_code = data.get("course_code")
    start_date = data.get("start_date")

    if not all([course_name, course_code, start_date]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        course = manager.create_course(course_name, course_code, start_date)
        return jsonify(course), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/create_modules', methods=['POST'])
def create_modules():
    data = request.json
    course_id = data.get("course_id")
    modules = data.get("modules")

    if not all([course_id, modules]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        module_ids = manager.create_modules(course_id, modules)
        return jsonify({"module_ids": module_ids}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/create_assignments', methods=['POST'])
def create_assignments():
    data = request.json
    course_id = data.get("course_id")
    assignments = data.get("assignments")

    if not all([course_id, assignments]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        manager.create_assignments(course_id, assignments)
        
        return jsonify({"message": "Assignments created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/create_quizzes', methods=['POST'])
def create_quizzes():
    data = request.json
    course_id = data.get("course_id")
    quizzes = data.get("quizzes")

    if not all([course_id, quizzes]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        manager.create_quizzes(course_id, quizzes)
        return jsonify({"message": "Quizzes created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/configure_module_release_dates', methods=['POST'])
def configure_module_release_dates():
    data = request.json
    course_id = data.get("course_id")
    module_ids = data.get("module_ids")
    start_date = data.get("start_date")
    interval_weeks = data.get("interval_weeks", 1)

    if not all([course_id, module_ids, start_date]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        start_date = datetime.fromisoformat(start_date)  # Parse ISO 8601 date format
        manager.configure_module_release_dates(course_id, module_ids, start_date, interval_weeks)
        return jsonify({"message": "Module release dates configured successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Flask Routes
@app.route("/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    return jsonify(user_manager.get_course(course_id))

@app.route("/users", methods=["GET"])
def get_user():
    user_identifier = request.args.get("user_identifier")
    if not user_identifier:
        return jsonify({"error": "User identifier is required"}), 400
    return jsonify(user_manager.get_user_info(user_identifier))

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and email are required"}), 400
    return jsonify(user_manager.create_user(data["name"], data["email"]))

@app.route("/courses/<int:course_id>/enroll", methods=["POST"])
def enroll_user(course_id):
    data = request.json
    if not data or "user_identifier" not in data:
        return jsonify({"error": "User identifier is required"}), 400
    return jsonify(user_manager.enroll_user(course_id, data["user_identifier"]))

@app.route("/courses/<int:course_id>/enrollments", methods=["GET"])
def fetch_enrollments(course_id):
    return jsonify(user_manager.fetch_enrolled_users(course_id))


@app.route('/api/fetch_user_progress', methods=['GET'])
def api_fetch_user_progress():
    course_id = request.args.get("course_id")
    user_id = request.args.get("user_id")

    # Validate inputs
    if not course_id or not user_id:
        return jsonify({"error": "Missing required query parameters: course_id and user_id"}), 400

    try:
        progress = user_manager.fetch_user_progress(course_id, user_id)
        if progress:
            return jsonify(progress), 200
        else:
            return jsonify({"error": "Failed to fetch user progress"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/progress_report', methods=['GET'])
def get_progress_report():
    course_id = request.args.get('course_id')
    if not course_id:
        return jsonify({"error": "Course ID is required"}), 400

    try:
        progress_data = user_manager.generate_progress_report(course_id)
        return jsonify(progress_data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to generate progress report: {str(e)}"}),


if __name__ == "__main__":
    app.run(debug=True)

