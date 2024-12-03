import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    API_URL = os.getenv("API_URL")
    API_TOKEN = os.getenv("API_TOKEN")
    ACCOUNT_ID = os.getenv("ACCOUNT_ID")
    FORM_API_URL = os.getenv('FORM_API_URL')
    FORM_CLIENT_ID = os.getenv('FORM_CLIENT_ID')
    FORM_CLIENT_SECRET = os.getenv('FORM_SECRET')
    REDIRECT_URL = os.getenv('REDIRECT_URL')
    CANVAS_CLIENT_SECRET = os.getenv('CANVAS_CLIENT_SECRET')
