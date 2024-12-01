from flask import Blueprint, request, jsonify
from models.forms import FormProcess
from config import Config

form_routes = Blueprint('form_routes', __name__)

form_handler = FormProcess(Config.FORM_API_URL, Config.FORM_TOKEN, Config.SECRET)


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

