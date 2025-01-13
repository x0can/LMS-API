from flask import Blueprint, request, jsonify, redirect
from models.forms import FormProcess
from config import Config
from flasgger.utils import swag_from


form_routes = Blueprint('form_routes', __name__)


form_handler = FormProcess(
    Config.FORM_API_URL,
    Config.FORM_CLIENT_ID,
    Config.FORM_CLIENT_SECRET,
    Config.REDIRECT_URL_FORM  # Always set this as '/api/callback'
)


@form_routes.route('/api/formstack/authorize')
@swag_from({
    "tags": ["FormStack AOth2 GET"],

    'responses': {
        200: {
            'description': 'Redirects to the authorization URL to start OAuth2 flow',
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
    Automaticaly redirects to the authorization URL to start the OAuth2 flow.
    """
    auth_url = form_handler.authorize_aouth2()

    if auth_url:
        return redirect(auth_url)  # Redirect the user to the authorization URL
    return "Failed to generate authorization URL."


# Always set this as 'redirect_url'
@form_routes.route('/api/formstack/callback', methods=['GET', 'POST'])
@swag_from({
    "tags": ["FormStack AOth2 Callback Endpoint"],

    'parameters': [
        {
            'name': 'code',
            'in': 'query',
            'description': 'Authorization code returned by the OAuth2 provider',
            'required': False,
            'schema': {
                'type': 'string'
            }
        },
        {
            'name': 'access_token',
            'in': 'body',
            'description': 'Access token from OAuth2 provider (for POST requests)',
            'required': False,
            'schema': {
                'type': 'string'
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Authorization successful and token returned',
            'schema': {
                'type': 'object'
            }
        },
        400: {
            'description': 'Failed to retrieve authorization code or access token',
            'schema': {
                'type': 'object'
            }
        },
        500: {
            'description': 'Internal server error processing the callback',
            'schema': {
                'type': 'object'
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
            form_handler.handle_redirect_callback_code(auth_code)

            token_data = form_handler.get_oauth2_token()

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
            status = form_handler.handle_token(access_token)
            return jsonify(status), 200

        else:
            return "Authorization failed.", 500


@form_routes.route('/api/formstack/submit_form', methods=['POST'])
@swag_from({
    "tags": ["Submit Form to FormStack API"],

    'parameters': [
        {
            'name': 'form_data',
            'in': 'body',
            'description': 'Form data to submit',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'form_id': {'type': 'string'},
                    'name': {'type': 'string'},
                    'type': {'type': 'string'},
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'email': {'type': 'string', 'format': 'email'},
                    'gender': {'type': 'string'},
                    'from_location': {'type': 'string'},
                    'source': {'type': 'string'},
                    'employment_status': {'type': 'string'},
                    'start_date': {'type': 'string', 'format': 'date'},
                    'education_level': {'type': 'string'},
                    'institution': {'type': 'string'},
                    'area_of_study': {'type': 'string'},
                    'professional_background': {'type': 'string'},
                    'industry': {'type': 'string'},
                    'kin_name': {'type': 'string'},
                    'kin_phone': {'type': 'string'},
                    'kin_email': {'type': 'string', 'format': 'email'},
                    'consent': {'type': 'boolean'}
                },
                'required': [
                    'form_id', 'name', 'type', 'first_name', 'last_name', 'email',
                    'gender', 'from_location', 'source', 'employment_status',
                    'start_date', 'education_level', 'institution', 'area_of_study',
                    'professional_background', 'industry', 'kin_name', 'kin_phone',
                    'kin_email', 'consent'
                ]
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Form submitted successfully',
            'schema': {
                'type': 'object'
            }
        },
        400: {
            'description': 'Missing required fields in form data',
            'schema': {
                'type': 'object'
            }
        },
        500: {
            'description': 'Failed to submit form',
            'schema': {
                'type': 'object'
            }
        }
    }
})
def submit_form():
    data = request.json

    # Validate the required fields in the form data
    required_fields = [
        "form_id",
        "name",
        "type",
        "first_name", "last_name", "email", "gender", "from_location", "source",
        "employment_status", "start_date", "education_level", "institution",
        "area_of_study", "professional_background", "industry", "kin_name",
        "kin_phone", "kin_email", "consent"
    ]

    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing required fields. {missing_fields}"}), 400

    try:
        # Call the submit_form_data method to send the data
        response_data, status_code = form_handler.submit_formstack_application(
            data['form_id'], data)

        return jsonify(response_data), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
