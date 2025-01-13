from flask import Blueprint, request, jsonify, redirect
from datetime import datetime
from config import Config
from models.courses import CourseManager
from flasgger.utils import swag_from


course_routes = Blueprint('course_routes', __name__)


course_manager = CourseManager(
    Config.CANVAS_URL, Config.CLIENT_ID,
    Config.REDIRECT_URL_CANVAS,  # Always set to /api/canvas/callback
    Config.CANVAS_CLIENT_SECRET,
    None,
    Config.API_TOKEN
)


@course_routes.route('/api/canvas/authorize')
@swag_from({
    'responses': {
        200: {
            'description': 'Redirects to the authorization URL for OAuth2 flow',
            'schema': {
                'type': 'string'
            }
        },
        500: {
            'description': 'Failed to generate authorization URL',
            'schema': {
                'type': 'string'
            }
        }
    }
})
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
@swag_from({
    'responses': {
        200: {
            'description': 'OAuth2 authorization code handled and token retrieved successfully',
            'schema': {
                'type': 'string'
            }
        },
        400: {
            'description': 'Authorization failed or missing parameters',
            'schema': {
                'type': 'string'
            }
        },
        500: {
            'description': 'Failed to retrieve or handle the token',
            'schema': {
                'type': 'string'
            }
        }
    }
})
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

        access_token = data.get('access_token') if data else None
        if access_token:
            status = course_manager.handle_token(access_token)
            return jsonify(status), 200

        else:
            return "Authorization failed.", 500


@course_routes.route('/api/canvas/create_course', methods=['GET'])
def get_account_id():
    course = course_manager.get_account_id()
    return jsonify(course), 201


@course_routes.route('/api/canvas/create_course', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'course_name',
            'in': 'body',
            'description': 'Name of the course',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'course_code',
            'in': 'body',
            'description': 'Code of the course',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'start_date',
            'in': 'body',
            'description': 'Start date of the course',
            'required': True,
            'schema': {
                'type': 'string',
                'format': 'date-time'
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Course created successfully',
            'schema': {
                'type': 'object'
            }
        },
        400: {
            'description': 'Missing required fields',
            'schema': {
                'type': 'object'
            }
        },
        500: {
            'description': 'Failed to create course',
            'schema': {
                'type': 'object'
            }
        }
    }
})
def create_course():

    data = request.json

    course_name = data.get("course_name")
    course_code = data.get("course_code")
    start_date = data.get("start_date")

    if not all([course_name, course_code, start_date]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        course = course_manager.create_course(
            course_name, start_date, 'public', course_code)

        return jsonify(course), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@course_routes.route('/api/canvas/create_modules', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'course_id',
            'in': 'body',
            'description': 'ID of the course',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        },
        {
            'name': 'module_name',
            'in': 'body',
            'description': 'Name of the module to create',
            'required': True,
            'schema': {
                'type': 'string'
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Module created successfully',
            'schema': {
                'type': 'object'
            }
        },
        400: {
            'description': 'Missing required fields',
            'schema': {
                'type': 'object'
            }
        },
        500: {
            'description': 'Failed to create module',
            'schema': {
                'type': 'object'
            }
        }
    }
})
def create_modules():

    data = request.json
    course_id = data.get("course_id")
    module_name = data.get("module_name")

    if not all([course_id, module_name]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        module = course_manager.create_module(course_id, module_name)
        return jsonify(module), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@course_routes.route('/api/canvas/create_assignment', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'course_id',
            'in': 'body',
            'description': 'ID of the course',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        },
        {
            'name': 'assignment_name',
            'in': 'body',
            'description': 'Name of the assignment to create',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'module_id',
            'in': 'body',
            'description': 'ID of the module to associate the assignment with',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Assignment created successfully',
            'schema': {
                'type': 'object'
            }
        },
        400: {
            'description': 'Missing required fields',
            'schema': {
                'type': 'object'
            }
        },
        500: {
            'description': 'Failed to create assignment',
            'schema': {
                'type': 'object'
            }
        }
    }
})
def create_assignments():

    data = request.json
    course_id = data.get("course_id")
    assignment_name = data.get("assignment_name")
    module_id = data.get("module_id")

    if not all([course_id, assignment_name, module_id]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        course_manager.create_assignments(
            course_id, assignment_name, module_id)

        return jsonify({"message": "Assignments created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@course_routes.route('/api/canvas/create_quizz', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'course_id',
            'in': 'body',
            'description': 'ID of the course',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        },
        {
            'name': 'module_id',
            'in': 'body',
            'description': 'ID of the module',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        },
        {
            'name': 'title',
            'in': 'body',
            'description': 'Title of the quiz',
            'required': True,
            'schema': {
                'type': 'string'
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Quiz created successfully',
            'schema': {
                'type': 'object'
            }
        },
        400: {
            'description': 'Missing required fields',
            'schema': {
                'type': 'object'
            }
        },
        500: {
            'description': 'Failed to create quiz',
            'schema': {
                'type': 'object'
            }
        }
    }
})
def create_quizzes():

    data = request.json
    course_id = data.get("course_id")
    module_id = data.get("module_id")
    title = data.get("title")

    if not all([course_id, title, module_id]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        course_manager.create_quiz(course_id, title, module_id)
        return jsonify({"message": "Quizze created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@course_routes.route('/api/canvas/configure_module_release_date', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'course_id',
            'in': 'body',
            'description': 'ID of the course',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        },
        {
            'name': 'module_id',
            'in': 'body',
            'description': 'ID of the module to configure release date for',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        },
        {
            'name': 'start_date',
            'in': 'body',
            'description': 'Start date of the module release',
            'required': True,
            'schema': {
                'type': 'string',
                'format': 'date-time'
            }
        },
        {
            'name': 'interval',
            'in': 'body',
            'description': 'Interval in weeks between module releases',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Module release date configured successfully',
            'schema': {
                'type': 'object'
            }
        },
        400: {
            'description': 'Missing required fields',
            'schema': {
                'type': 'object'
            }
        },
        500: {
            'description': 'Failed to configure module release date',
            'schema': {
                'type': 'object'
            }
        }
    }
})
def configure_module_release_dates():

    data = request.json
    course_id = data.get("course_id")
    module_id = data.get("module_id")
    start_date = data.get("start_date")
    interval_week = data.get('interval')

    if not all([course_id, module_id, start_date, interval_week]):
        return jsonify({"error": "Missing required fields"}), 400

    try:

        start_date = datetime.fromisoformat(start_date)
        course_manager.configure_module_release_dates(
            course_id, module_id, start_date, interval_week)
        return jsonify({"message": "Module release date configured successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@course_routes.route("/api/canvas/users", methods=["POST"])
@swag_from({
    'parameters': [
        {
            'name': 'name',
            'in': 'body',
            'description': 'Name of the user to create',
            'required': True,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'email',
            'in': 'body',
            'description': 'Email of the user to create',
            'required': True,
            'schema': {
                'type': 'string',
                'format': 'email'
            }
        }
    ],
    'responses': {
        201: {
            'description': 'User created successfully',
            'schema': {
                'type': 'object'
            }
        },
        400: {
            'description': 'Missing required fields',
            'schema': {
                'type': 'object'
            }
        },
        500: {
            'description': 'Failed to create user',
            'schema': {
                'type': 'object'
            }
        }
    }
})
def create_user():

    data = request.json
    name = data.get('name')
    email = data.get('email')

    if not all([name, email]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        return jsonify(course_manager.create_user(name, email))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@course_routes.route("/api/canvas/courses/<int:course_id>/enroll", methods=["POST"])
@swag_from({
    'parameters': [
        {
            'name': 'user_identifier',
            'in': 'body',
            'description': 'User identifier to enroll in the course',
            'required': True,
            'schema': {
                'type': 'string'
            }
        }
    ],
    'responses': {
        200: {
            'description': 'User enrolled successfully',
            'schema': {
                'type': 'object'
            }
        },
        400: {
            'description': 'Missing user identifier',
            'schema': {
                'type': 'object'
            }
        },
        500: {
            'description': 'Failed to enroll user',
            'schema': {
                'type': 'object'
            }
        }
    }
})
def enroll_user(course_id):

    try:
        data = request.json
        if not data or "user_identifier" not in data:
            return jsonify({"error": "User identifier is required"}), 400
        return jsonify(course_manager.enroll_user(course_id, data))
    except Exception as e:
        print('error')
        return jsonify({"error": str(e)}), 500


@course_routes.route("/api/canvas/courses/<int:course_id>/enrollments", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'List of users enrolled in the course',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object'
                }
            }
        },
        500: {
            'description': 'Failed to fetch enrollments',
            'schema': {
                'type': 'object'
            }
        }
    }
})
def fetch_enrollments(course_id):
    try:
        return jsonify(course_manager.fetch_enrolled_users(course_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@course_routes.route('/api/canvas/fetch_user_progress', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'course_id',
            'in': 'query',
            'description': 'ID of the course to fetch user progress for',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        },
        {
            'name': 'user_id',
            'in': 'query',
            'description': 'ID of the user to fetch progress for',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        }
    ],
    'responses': {
        200: {
            'description': 'User progress retrieved successfully',
            'schema': {
                'type': 'object'
            }
        },
        400: {
            'description': 'Missing required query parameters',
            'schema': {
                'type': 'object'
            }
        },
        404: {
            'description': 'User progress not found',
            'schema': {
                'type': 'object'
            }
        },
        500: {
            'description': 'Failed to fetch user progress',
            'schema': {
                'type': 'object'
            }
        }
    }
})
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


@course_routes.route('/api/canvas/progress_report', methods=['GET'])
def get_progress_report():
    course_id = request.args.get('course_id')
    if not course_id:
        return jsonify({"error": "Course ID is required"}), 400

    try:
        progress_data = course_manager.generate_progress_report(course_id)
        return jsonify(progress_data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to generate progress report: {str(e)}"}),
