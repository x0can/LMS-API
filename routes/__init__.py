from routes.course import course_routes
from routes.forms import form_routes
from routes.reports import report_routes
from flasgger import Swagger



def configure_routes(app):

    app.register_blueprint(course_routes)
    app.register_blueprint(form_routes)
    app.register_blueprint(report_routes)
    Swagger(app)
