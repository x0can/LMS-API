from flask import Blueprint, request, jsonify, redirect
from datetime import datetime
from config import Config
from models.courses import CourseManager


course_routes = Blueprint('course_routes', __name__)


course_manager = CourseManager(
    Config.API_URL, Config.ACCOUNT_ID,
    "http://localhost:5000/api/canvas/callback",
    Config.CANVAS_CLIENT_SECRET
)


@course_routes.route('/api/canvas/authorize')
def authorize():
    """
    Automaticall redirects to the authorization URL to start the OAuth2 flow.
    """
    auth_url = course_manager.authorize_aouth2()

    if auth_url:
        return redirect(auth_url)  # Redirect the user to the authorization URL
    return "Failed to generate authorization URL."


# Always set this as 'redirect_url'
@course_routes.route('/api/canvas/callback', methods=['GET', 'POST'])
def callback():
    """
    Handles the OAuth2 redirect callback and processes the authorization code.
    """

    # Check if the request is a GET or POST request
    if request.method == 'GET':
        # Handle query parameters (like 'code')
        auth_code = request.args.get('code')
        if auth_code:
            course_manager.handle_redirect_callback_code(auth_code)

            token_data = course_manager.get_oauth2_token()

            if token_data:
                # Return the full token data
                return f"Authorization successful. You can close this window.\n {jsonify(token_data)}"
            else:
                return "Failed to retrieve the access token.", 500
        else:
            return "Authorization failed."

    elif request.method == 'POST':
        # Handle JSON payload
        data = request.get_json()

        auth_code = data.get('code') if data else None
        if auth_code:
            course_manager.handle_redirect_callback_code(auth_code)

            token_data = course_manager.get_oauth2_token()

            if token_data:
                # Return the full token data
                return jsonify(token_data)
            else:
                return "Failed to retrieve the access token.", 500
        else:
            return "Authorization failed."


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




@course_routes.route("/api/users", methods=["POST"])
def create_user():

    try:
        data = request.json
        if not data or "name" not in data or "email" not in data:
            return jsonify({"error": "Name and email are required"}), 400
        return jsonify(course_manager.create_user(data["name"], data["email"]))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@course_routes.route("/api/courses/<int:course_id>/enroll", methods=["POST"])
def enroll_user(course_id):

    try:
        data = request.json
        if not data or "user_identifier" not in data:
            return jsonify({"error": "User identifier is required"}), 400
        return jsonify(course_manager.enroll_user(course_id, data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@course_routes.route("/api/courses/<int:course_id>/enrollments", methods=["GET"])
def fetch_enrollments(course_id):
    try:
        return jsonify(course_manager.fetch_enrolled_users(course_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@course_routes.route('/api/fetch_user_progress', methods=['GET'])
def api_fetch_user_progress():
    course_id = request.args.get("course_id")
    user_id = request.args.get("user_id")

    # Validate inputs
    if not course_id or not user_id:
        return jsonify({"error": "Missing required query parameters: course_id and user_id"}), 400

    try:
        progress = course_manager.fetch_user_progress(course_id, user_id)
        if progress:
            return jsonify(progress), 200
        else:
            return jsonify({"error": "Failed to fetch user progress"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@course_routes.route('/api/progress_report', methods=['GET'])
def get_progress_report():
    course_id = request.args.get('course_id')
    if not course_id:
        return jsonify({"error": "Course ID is required"}), 400

    try:
        progress_data = course_manager.generate_progress_report(course_id)
        return jsonify(progress_data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to generate progress report: {str(e)}"}),
