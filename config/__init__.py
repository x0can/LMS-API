import os

from dotenv import load_dotenv

# Unset previously loaded environment variables
os.environ.clear()

# Reload the .env file
load_dotenv()


class Config:
    CANVAS_URL = os.getenv("CANVAS_URL")
    API_TOKEN = os.getenv("API_TOKEN")
    CLIENT_ID = os.getenv("CLIENT_ID")
    FORM_API_URL = os.getenv('FORM_API_URL')
    FORM_CLIENT_ID = os.getenv('FORM_CLIENT_ID')
    FORM_CLIENT_SECRET = os.getenv('FORM_SECRET')
    REDIRECT_URL_FORM = os.getenv('REDIRECT_URL_FORM')
    CANVAS_CLIENT_SECRET = os.getenv('CANVAS_CLIENT_SECRET')
    REDIRECT_URL_CANVAS= os.getenv('REDIRECT_URL_CANVAS')
