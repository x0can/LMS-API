import requests
from requests.auth import HTTPBasicAuth


class FormProcess:
    def __init__(self, api_url, token, secret):
        self.api_url = api_url
        self.token = token
        self.secret = secret
        self.session = requests.Session()


    def submit_form_data(self, form_data):

        headers = {
            "Content-Type": "application/json"
        }
        

        try: 
            auth = HTTPBasicAuth(self.token, self.secret)
            response = self.session.post(
                self.api_url, json=form_data, headers=headers, auth=auth)

            # Check if the response is successful (status 200)
            if response.status_code == 200:
                try:
                    return response.json(), 200
                except ValueError:
                    return {"error": "Empty or invalid JSON response from API"}, 500
            else:
                # Handle error response
                try:
                    error_response = response.json()
                    error_message = error_response.get(
                        'error', 'An error occurred')
                except ValueError:
                    error_message = 'Error occurred but no JSON response provided'

                return {"error": error_message, "status_code": response.status_code}, response.status_code

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}, 500

