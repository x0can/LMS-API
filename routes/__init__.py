from routes.users import user_routes
from routes.course import course_routes
from routes.forms import forms_routes


def configure_routes(app):
    app.register_blueprint(user_routes)
    app.register_blueprint(course_routes)
    app.register_blueprint(forms_routes)
