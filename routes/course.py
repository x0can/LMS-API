from flask import Blueprint, request, jsonify
from datetime import datetime
from config import Config
from models.courses import CourseManager
from models.users import CanvasUserManager


course_routes = Blueprint('course_routes', __name__)

user_manager = CanvasUserManager(Config.API_URL, Config.API_TOKEN, Config.ACCOUNT_ID)
course_manager = CourseManager(Config.API_URL, Config.API_TOKEN, Config.ACCOUNT_ID, user=user_manager)


@course_routes.route('/api/create_course', methods=['POST'])
def create_course():
    
    permissions =  user_manager.get_user_permissions(permissions=['manage_courses_admin'])
    
    
    data = request.json
    course_name = data.get("course_name")
    course_code = data.get("course_code")
    start_date = data.get("start_date")

    if permissions:
        if not all([course_name, course_code, start_date]):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            course = course_manager.create_course(course_name, course_code, start_date)
            return jsonify(course), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@course_routes.route('/api/create_modules', methods=['POST'])
def create_modules():
    
    permissions = user_manager.get_user_permissions(permissions=['manage_courses_admin'])
    
    if permissions:
        data = request.json
        course_id = data.get("course_id")
        modules = data.get("modules")

        if not all([course_id, modules]):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            module_ids = course_manager.create_modules(course_id, modules)
            return jsonify({"module_ids": module_ids}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    return 'Not possible to perform this action'    
    

@course_routes.route('/api/create_assignments', methods=['POST'])
def create_assignments():
    permissions= user_manager.get_user_permissions(permissions=['manage_courses_admin'])

    if permissions:
        data = request.json
        course_id = data.get("course_id")
        assignments = data.get("assignments")

        if not all([course_id, assignments]):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            course_manager.create_assignments(course_id, assignments)
            
            return jsonify({"message": "Assignments created successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return 'Not possible to perform this action'    

@course_routes.route('/api/create_quizzes', methods=['POST'])
def create_quizzes():
    permissions= user_manager.get_user_permissions(permissions=['manage_courses_admin'])

    if permissions:  
        data = request.json
        course_id = data.get("course_id")
        quizzes = data.get("quizzes")

        if not all([course_id, quizzes]):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            course_manager.create_quizzes(course_id, quizzes)
            return jsonify({"message": "Quizzes created successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return 'Not possible to perform this action'    


@course_routes.route('/api/configure_module_release_dates', methods=['POST'])
def configure_module_release_dates():
    permissions= user_manager.get_user_permissions(permissions=['manage_courses_admin'])

    if permissions:
        data = request.json
        course_id = data.get("course_id")
        module_id = data.get("module_id")
        start_date = data.get("start_date")

        

        try:
            start_date = datetime.fromisoformat(start_date) 
            course_manager.configure_module_release_dates(course_id, module_id, start_date,1)
            return jsonify({"message": "Module release dates configured successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    return 'Not possible to perform this action'    


