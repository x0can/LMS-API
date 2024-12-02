from flask import Blueprint, request, jsonify, redirect
from models.forms import FormProcess
from config import Config

form_routes = Blueprint('form_routes', __name__)


form_handler = FormProcess(
    Config.FORM_API_URL,
    Config.FORM_CLIENT_ID,
    Config.FORM_CLIENT_SECRET,
    "http://localhost:5000/api/callback"  # Always set this as '/api/callback'
)


@form_routes.route('/api/authorize')
def authorize():
    """
    Automaticall redirects to the authorization URL to start the OAuth2 flow.
    """
    auth_url = form_handler.authorize_aouth2()

    if auth_url:
        return redirect(auth_url)  # Redirect the user to the authorization URL
    return "Failed to generate authorization URL."


#Always set this as 'redirect_url'
@form_routes.route('/api/callback', methods=['GET', 'POST'])
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

        auth_code = data.get('code') if data else None
        if auth_code:
            form_handler.handle_redirect_callback_code(auth_code)

            token_data = form_handler.get_oauth2_token()

            if token_data:
                # Return the full token data
                return jsonify(token_data)
            else:
                return "Failed to retrieve the access token.", 500
        else:
            return "Authorization failed."


@form_routes.route('/api/submit_form', methods=['POST'])
def submit_form():
    data = request.json

    # Validate the required fields in the form data
    required_fields = [
        "form_id"
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
