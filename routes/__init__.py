from routes.course import course_routes
from routes.forms import form_routes


def configure_routes(app):
    app.register_blueprint(course_routes)
    app.register_blueprint(form_routes)
