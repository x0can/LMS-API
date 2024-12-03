Question 3
==

The Formstack student application form to collect applicants' information listed below
1. Personal Details
 	-  a. First Name
 	-  b. Last Name
 	-  c. Email
 	-  d. Gender
 	-  e. Where are you from?
 	-  f. How did you hear about Moringa School?
 	-  g. Current Employment Status
 	-  h. Class Start Date

2. Professional Background
	- a. What is your highest level of education completed?
	- b. What is the name of the institution you attended
	- c. Please select your area of study from the following
	- d. How would you describe your 	professional background?
	- e. Please select your industry from the following

3. Next of Kin Details
	- a. Name
	- b. Phone Number
	- c. Email
	- d. Data Processing Consent[checkbox]

- A. Write a query that submits the form with an applicant's bio-data via API

- B. Provide a sample JavaScript snippet to validate the start date (ensuring it’s at least two weeks from the current date).


## Solution

   
- [How to submit an applicant's bio-data via API](#How-to-submit-an-applicants-bio-data-via-API)

Referrence material: https://developers.formstack.com/docs/getting-started


- First let's update our code structure, since I'm using a single repository, this is the approach I choose to organise my files


```
    client
        handlers.js
        index.js
        index.html

    config
        __init__.py
    models
       courses.py
       forms.py
    
    routes
        __init__.py
        courses.py
        forms.py
    main.py
    .env
    .gitignore
    requirements.txt
    
``` 

update the .env file

```
FORM_API_URL=YOUR_FORM_API_URL
FORM_CLIENT_ID=YOUR_FORM_CLIENT_ID
FORM_CLIENT_SECRET=YOUR_FORM_CLIENT_SECRET
REDIERCT_URL=REDIERCT_URL
```

To follow along

git clone this repository: https://github.com/x0can/LMS-API

Navigate to formstack admin page and obtain the above environment variables

Next 

`pip3 install -r requirements.txt`

`python3 main.py`

On your browser send this request to obtain redirect_url for generating `auth token`
```
GET  http://127.0.0.1:5000/api/authorize
```



### How to submit an applicant's bio-data via API


Requirements and Assumptions:

1. Need to be an Admin to create an application on FormStack and obtain configurations
2. Follow through this process on how to get Admin API environment variable 
`FORM_API_URL,
    FORM_CLIENT_ID,
    FORM_CLIENT_SECRET,
    REDIRECT_URL,
    `
    
    Formstack Aouth2: https://developers.formstack.com/reference/oauth2-authorize-get
    
- First we need to obtain an OAuth2 token for us to proceed. 

Reference material: https://developers.formstack.com/reference/oauth2-token-post

Before genearating the token, let's create a `callback` url that will work as our `redirect_url`. It will handle the flow where you first get the authorization code from the URL and then exchange it for the OAuth2 token using the `get_oauth2_token` method below, returning all the relevant token data in the response.


Steps
1. Generate the authorization URL and prompt the user to visit it
2. The user is redirected 
3. Extract `code` from the URL and store it
4. Use the `code` to retrieve the OAuth2 token

github: https://github.com/x0can/LMS-API/blob/main/models/forms.py


```
GET  /api/v2/oauth2/authorize"
POST /api/v2/oauth2/token 
```



models.forms.py
```python=-
import requests


class FormProcess:
    def __init__(self, api_url, client_id, client_secret, redirect_uri, code=None,access_token=None):
        self.api_url = api_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.code = code
        self.access_token=access_token
        self.headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }


    def handle_redirect_callback_code(self, code):
        self.code = code
        return code

    def authorize_aouth2(self):

        endpoint = f"{self.api_url}/api/v2/oauth2/authorize"
        try:
            # Construct the authorization URL
            auth_url = f"{endpoint}?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code"
            return auth_url

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error generating OAuth2 token {str(e)}")

    def get_oauth2_token(self):
        """
        Generates an OAuth2 token using the Formstack API.
        """

        if not self.code:
            return "Authorization code is missing. Please authorize first."

        # Define endpoint and payload
        endpoint = f"{self.api_url}/oauth2/token"
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": self.code
        }

        try:
            # Send POST request to get the token
            response = requests.post(endpoint, data=payload)

            # Raise an error if the request failed
            response.raise_for_status()

            # Return the access token if successful
            token_data = response.json()
            access_token = token_data.get('access_token')
            self.access_token = access_token
            
            return self.access_token
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error generating OAuth2 token {str(e)}")
            
    def handle_token(self, access_token):
        self.access_token = access_token
        return "Authorization Successfull"            
```

routes.forms.py

```python=
from flask import Blueprint, request, jsonify, session
from models.forms import FormProcess
from config import Config

form_routes = Blueprint('form_routes', __name__)


form_handler = FormProcess(
    Config.FORM_API_URL,
    Config.FORM_CLIENT_ID,
    Config.FORM_CLIENT_SECRET,
    Config.REDIRECT_URL # Always set this as '/api/callback'
)


@form_routes.route('/api/authorize')
def authorize():
    """
    Auto redirects to the authorization URL to start the OAuth2 flow.
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

        access_token = data.get('access_token') if data else None
        if access_token:
            status =  form_handler.handle_token(access_token)
            return jsonify(status), 200
            
        else:
            return "Authorization failed.", 500


```


- Next we create the `POST` request to submit applicants data

Referrence material: https://developers.formstack.com/reference/submissions

```
POST api/v2/form/{id}/submission.json
```

Assumptions: Data validation is handled on the client, you can skip to check [here](#How-to-Validate-the-start-date) how the start date is validated to make sure it's at least two weeks from the current date

models.forms.py
```python=
class FormProcess:

...
        def submit_formstack_application(self, form_id, applicant_data):
            """
            Submits an application to the Formstack API using OAuth2 tokens.
            """
            # Endpoint for form submissions
            endpoint = f"{self.api_url}/form/{form_id}/submission.json"

            try:

                #get access_token
                access_token = self.get_oauth2_token()

                # Define headers for authentication
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                }

                # Send POST request to Formstack
                response = requests.post(endpoint, json=applicant_data, headers=headers)

                # Raise an error if the request failed
                response.raise_for_status()

                # Return the JSON response if successful
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error submitting the form: {e}")
                return None


```

When testing you might incur the following error,`Authorization code is missing. Please authorize first.` 

If you do, send a request to this endpoint

```
GET Http://Your-local-host/api/authorize
```

Then resume the process

create the '/submit-form' endpoint

routes.forms.py
```python=

...
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


```



### How to Validate the start date


Validate data before sending the `POST` request to the API endpoint `/api/submit-form` above using JavaScript

process

- Create an input validation function to check if the date is two weeks from current date
- Check if applicant's start date is okay and
- Send a `POST` request to our backend



Test by starting a server on the following path `/clients/index.html`

Or simply open the html file on a browser.



client.handlers.js
```javascript=
/**
 * Validates the start date to ensure it’s at least two weeks from the current date.
 * @param {string} startDate - The date to be validated in 'YYYY-MM-DD' format.
 * @returns {boolean} - Returns true if the start date is valid, false otherwise.
 */

// validator

const validateStartDate = (startDate) => {
  const today = new Date();
  const startDateObj = new Date(startDate);
  const twoWeeksFromToday = new Date(today);
  twoWeeksFromToday.setDate(today.getDate() + 14); // Set date to 14 days from today

  // Early return if the start date is invalid
  return (
    startDateObj >= twoWeeksFromToday || {
      error: "Start date must be at least 14 days from today.",
    }
  );
};

/**
 * Submits the form to the following endpoint {url}/submit_form.
 * @param {object} formData - The form data to send over to the API.
 * @param {string} url - The API endpoint url, must match the server's endpoint.
 * @returns {object} - Returns object if successful, error otherwise.
 */

// handlers

const submitForm = async (formData, url) => {
  // Validate form data
  validDate = validateStartDate(formData["start_date"]);

  // If validation fails (validDate is an object with an error), return the error
  if (validDate.error) {
    return validDate; 
  }
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || "Failed to submit form");
    }

    return result;
  } catch (error) {
    console.error("Error submitting form:", error.message);
    throw error;
  }
};



function handle_form() {
  const form = document.getElementById("submitForm");

  const url = "http://127.0.0.1:5000/api/submit_form";

  const formStatus = document.getElementById("formStatus");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = {
      form_id: 'F1O1',
      name: form.name.value,
      type: form.type.value,
      first_name: form.first_name.value,
      last_name: form.last_name.value,
      email: form.email.value,
      gender: form.gender.value,
      from_location: form.from_location.value,
      source: form.source.value,
      employment_status: form.employment_status.value,
      start_date: form.start_date.value,
      education_level: form.education_level.value,
      institution: form.institution.value,
      area_of_study: form.area_of_study.value,
      professional_background: form.professional_background.value,
      industry: form.industry.value,
      kin_name: form.kin_name.value,
      kin_phone: form.kin_phone.value,
      kin_email: form.kin_email.value,
      consent: form.consent.checked,
    };

    try {
      const result = await submitForm(url, formData);

      const { error } = result;

      if (error) {
        formStatus.textContent = error;
        formStatus.style.color = "#F44336";
      } else {
        formStatus.textContent = "Form submitted successfully!";
        formStatus.style.color = "green";
      }
    } catch (error) {
      console.log(error.message);
      formStatus.textContent = error.message;
      formStatus.style.color = "#F44336";
    }
  });
}

handle_form();


```
To test the above

Run a live server inside the `/clients/index.html` file then submit the form there.
