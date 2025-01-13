from routes.course import course_routes
from routes.forms import form_routes
from routes.reports import report_routes
from flasgger import Swagger
from config import Config


canvas_url = Config.CANVAS_URL
redirect_url_canvas = Config.REDIRECT_URL_CANVAS
canvas_client_secret = Config.CANVAS_CLIENT_SECRET
api_token = Config.API_TOKEN


swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,  # Include all endpoints
            "model_filter": lambda tag: True,  # Include all models
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/",
}

swagger_template = {
    "swagger_ui_parameters": {
            "canvas_url": canvas_url,
            "redirect_url_canvas": redirect_url_canvas,
            "canvas_client_secret": canvas_client_secret,
            "api_token": api_token
        },
    "info": {
        "title": "Custom API",
        "description": "This is an API middleware for interracting with Cannvas APi and FormStack API",
        "version": "1.0",
        "contact": {
            "name": "Alex Mwaura",
            "email": "alexmwaura43@gmail.com",
            "url": "#",
        },
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http"],
    "tags": [
        {
            "name": "Custom Endpoints",
            "description": "A group of custom endpoints",
        }
    ],
    
}


def configure_routes(app):

    app.register_blueprint(course_routes)
    app.register_blueprint(form_routes)
    app.register_blueprint(report_routes)
    Swagger(app, template=swagger_template, config=swagger_config, )
