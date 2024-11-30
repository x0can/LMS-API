from flask import Blueprint, request, jsonify

form_routes = Blueprint('form_routes', __name__)


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

    # Initialize the FormProcess instance with the API URL
    form_handler = FormProcess(FORM_API_URL, FORM_TOKEN, SECRET)

    # Call the submit_form_data method to send the data
    response_data, status_code = form_handler.submit_form_data(data)

    return jsonify(response_data), status_code



@form_routes.route('/get_form', methods=['GET'])
def get_form_data():
    form_handler = FormProcess(FORM_API_URL, FORM_TOKEN, SECRET)
    form_id = request.args.get("form_id")
    
    if not form_id:
        return jsonify({"error": "form_id is required"}), 400

    form_data, status_code = form_handler.get_form_data(form_id)
    
    return jsonify(form_data), status_code
