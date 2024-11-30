import requests
from requests.auth import HTTPBasicAuth


class FormProcess:
    def __init__(self, api_url, token, secret):
        self.api_url = api_url
        self.token = token
        self.secret = secret
        self.session = requests.Session()

    def authenticate(self):
        try:
            # Call the authentication endpoint with Basic Auth
            # Assuming /auth is the authentication endpoint
            auth_url = f"{self.api_url}/auth"
            response = self.session.get(
                auth_url, auth=HTTPBasicAuth(self.token, self.secret))

            print(
                f"Authentication response status code: {response.status_code}")

            # Check if the authentication was successful
            if response.status_code == 200:
                # Extract session cookies from the response headers
                cookies = response.cookies
                print(f"Session cookies: {cookies}")

                # Store the cookies in the session object
                self.session.cookies.update(cookies)

                print("Authentication successful, session cookies stored.")
                return True
            else:
                print(
                    f"Authentication failed with status code: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"Error during authentication: {str(e)}")
            return False

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

    def get_form_data(self, form_id):
        
        try:
            # Construct the URL for retrieving form data based on the form ID
            form_url = f"{self.api_url}/{form_id}"


            # Use basic authentication to fetch the form data
            auth = HTTPBasicAuth(self.token, self.secret)

            # Make the GET request to retrieve the form data
            response = self.session.get(form_url, auth=auth)


            if response.status_code == 200:
                try:
                    return response.json(), 200
                except ValueError:
                    return {"error": "Empty or invalid JSON response from API"}, 500
            else:
                try:
                    error_response = response.json()
                    error_message = error_response.get(
                        'error', 'An error occurred')
                except ValueError:
                    error_message = 'Error occurred but no JSON response provided'

                return {"error": error_message, "status_code": response.status_code}, response.status_code

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}, 500
