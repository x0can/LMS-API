from flask import Blueprint, request, jsonify
from datetime import datetime
from config import Config
from models.courses import CourseManager
from models.users import CanvasUserManager


course_routes = Blueprint('course_routes', __name__)

user_manager = CanvasUserManager(
    Config.API_URL, Config.API_TOKEN, Config.ACCOUNT_ID)
course_manager = CourseManager(
    Config.API_URL, Config.API_TOKEN, Config.ACCOUNT_ID, user=user_manager)



@course_routes.route('/api/create_course', methods=['POST'])
def create_course():

    data = request.json
    course_name = data.get("course_name")
    course_code = data.get("course_code")
    start_date = data.get("start_date")

    if not all([course_name, course_code, start_date]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        course = course_manager.create_course(
            course_name, course_code, start_date)
        return jsonify(course), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@course_routes.route('/api/create_modules', methods=['POST'])
def create_modules():

    data = request.json
    course_id = data.get("course_id")
    module_name = data.get("module_name")

    if not all([course_id, module_name]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        module = course_manager.create_modules(course_id, module_name)
        return jsonify(module), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@course_routes.route('/api/create_assignment', methods=['POST'])
def create_assignments():

    data = request.json
    course_id = data.get("course_id")
    assignment_name = data.get("assignment_name")
    assignment_name = data.get("assignment_name")

    if not all([course_id, assignment_name]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        course_manager.create_assignments(course_id, assignment_name)

        return jsonify({"message": "Assignments created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@course_routes.route('/api/create_quizz', methods=['POST'])
def create_quizzes():

    data = request.json
    course_id = data.get("course_id")
    title = data.get("title")

    if not all([course_id, title]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        course_manager.create_quiz(course_id, title)
        return jsonify({"message": "Quizze created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@course_routes.route('/api/configure_module_release_date', methods=['POST'])
def configure_module_release_dates():

    data = request.json
    course_id = data.get("course_id")
    module_id = data.get("module_id")
    start_date = data.get("start_date")
    interval_week = data.get('interval')

    try:
        start_date = datetime.fromisoformat(start_date)
        course_manager.configure_module_release_dates(
            course_id, module_id, start_date, interval_week)
        return jsonify({"message": "Module release date configured successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
