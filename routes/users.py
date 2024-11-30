from flask import Blueprint, request, jsonify
from users.model import CanvasUserManager


user_routes = Blueprint('user_routes', __name__)
user_manager = CanvasUserManager(API_URL, API_TOKEN, ACCOUNT_ID)
    

@user_routes.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and email are required"}), 400
    return jsonify(user_manager.create_user(data["name"], data["email"]))

@user_routes.route("/courses/<int:course_id>/enroll", methods=["POST"])
def enroll_user(course_id):
    data = request.json
    if not data or "user_identifier" not in data:
        return jsonify({"error": "User identifier is required"}), 400
    return jsonify(user_manager.enroll_user(course_id, data["user_identifier"]))

@user_routes.route("/courses/<int:course_id>/enrollments", methods=["GET"])
def fetch_enrollments(course_id):
    return jsonify(user_manager.fetch_enrolled_users(course_id))


@user_routes.route('/api/fetch_user_progress', methods=['GET'])
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


@user_routes.route('/api/progress_report', methods=['GET'])
def get_progress_report():
    course_id = request.args.get('course_id')
    if not course_id:
        return jsonify({"error": "Course ID is required"}), 400

    try:
        progress_data = user_manager.generate_progress_report(course_id)
        return jsonify(progress_data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to generate progress report: {str(e)}"}),


