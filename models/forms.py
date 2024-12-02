import requests


class FormProcess:
    def __init__(self, api_url, client_id, client_secret, redirect_uri, code=None, access_token=None):
        self.api_url = api_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.code = code
        self.access_token = access_token
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

    def submit_formstack_application(self, form_id, applicant_data):
        """
        Submits an application to the Formstack API using OAuth2 tokens.
        """
        # Endpoint for form submissions
        endpoint = f"{self.api_url}/form/{form_id}/submission"

        try:

            # Send POST request to Formstack
            response = requests.post(
                endpoint, json=applicant_data, headers=self.headers)

            # Raise an error if the request failed
            response.raise_for_status()

            # Return the JSON response if successful
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to submit form: {str(e)}")
