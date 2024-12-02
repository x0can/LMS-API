from flask import Blueprint, request, jsonify, redirect
from models.forms import FormProcess
from config import Config

form_routes = Blueprint('form_routes', __name__)


form_handler = FormProcess(
    Config.API_URL,
    Config.FORM_CLIENT_ID,
    Config.FORM_CLIENT_SECRET,
    "http://localhost:5000/callback" # Always set this as '/callback'
)


@form_routes.route('/authorize')
def authorize():
    """
    Automaticall redirects to the authorization URL to start the OAuth2 flow.
    """
    auth_url = form_handler.authorize_aouth2()

    if auth_url:
        return redirect(auth_url)  # Redirect the user to the authorization URL
    return "Failed to generate authorization URL."


@form_routes.route('/callback')
def callback():
    """
    Handles the OAuth2 redirect callback and processes the authorization code.
    The redirect_uri here will always be '/callback'.
    """    
    
   
        
    auth_code = request.args.get('code')
    if auth_code:
        
        form_handler.handle_redirect_callback_code(auth_code)

        token_data = form_handler.get_oauth2_token()
        
        if token_data:
            return f"Authorization successful. You can close this window.\n {jsonify(token_data)}"  # Return the full token data
        else:
            return "Failed to retrieve the access token.", 500
    
    else:
        return "Authorization failed."
        



@form_routes.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.json

    # Validate the required fields in the form data
    required_fields = [
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

    # Call the submit_form_data method to send the data
    response_data, status_code = form_handler.submit_form_data(data)

    return jsonify(response_data), status_code

