from flask import Blueprint, request, jsonify

course_routes = Blueprint('course_routes', __name__)

@course_routes.route('/api/create_course', methods=['POST'])
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

@course_routes.route('/api/create_modules', methods=['POST'])
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

@course_routes.route('/api/create_assignments', methods=['POST'])
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

@course_routes.route('/api/create_quizzes', methods=['POST'])
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

@course_routes.route('/api/configure_module_release_dates', methods=['POST'])
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


@course_routes.route("/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    return jsonify(user_manager.get_course(course_id))

@course_routes.route("/users", methods=["GET"])
def get_user():
    user_identifier = request.args.get("user_identifier")
    if not user_identifier:
        return jsonify({"error": "User identifier is required"}), 400
    return jsonify(user_manager.get_user_info(user_identifier))

