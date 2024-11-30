from flask import Flask, jsonify, request
import os
from datetime import datetime
from dotenv import load_dotenv
from config import Config
from routes import configure_routes


# Set up configuration for the Flask app
app = Flask(__name__)
app.config.from_object(Config)

# user_manager = UserModel(API_URL, API_TOKEN, ACCOUNT_ID)


# Register routes
configure_routes(app)


if __name__ == "__main__":
    app.run(debug=True)



