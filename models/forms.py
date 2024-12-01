import requests
from requests.auth import HTTPBasicAuth


class FormProcess:
    def __init__(self, api_url, client_id, client_secret, redirect_uri, code):
        self.api_url = api_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.code = code

    def get_oauth2_token(self):
        """
        Generates an OAuth2 token using the Formstack API.
        """

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
            return token_data.get("access_token")
        except requests.exceptions.RequestException as e:
            print(f"Error generating OAuth2 token: {e}")
            return None

    def submit_formstack_application(self, form_id, applicant_data):
        """
        Submits an application to the Formstack API using OAuth2 tokens.
        """
        # Endpoint for form submissions
        endpoint = f"{self.api_url}/form/{form_id}/submission"

        try:

            # get access_token
            access_token = self.get_oauth2_token()

            # Define headers for authentication
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            # Send POST request to Formstack
            response = requests.post(
                endpoint, json=applicant_data, headers=headers)

            # Raise an error if the request failed
            response.raise_for_status()

            # Return the JSON response if successful
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error submitting the form: {e}")
            return None
