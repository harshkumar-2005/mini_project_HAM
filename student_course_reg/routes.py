from flask import Blueprint, request, jsonify
from models import db, User, Course, Enrollment
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity, 
                                create_refresh_token, jwt_refresh_token_required)
from werkzeug.security import check_password_hash, generate_password_hash

routes_bp = Blueprint("routes_bp", __name__)

# Standardized response format
def response(success, message, data=None):
    return jsonify({"success": success, "message": message, "data": data}), 200 if success else 400

# Home Route
@routes_bp.route("/")
def home():
    return response(True, "Welcome to the Student Course Registration System!")

# User Login
@routes_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return response(False, "Missing email or password")
    
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return response(False, "Invalid credentials")
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return response(True, "Login successful", {"access_token": access_token, "refresh_token": refresh_token})

# Refresh Token
@routes_bp.route("/auth/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return response(True, "Token refreshed", {"access_token": new_access_token})

# Register User
@routes_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return response(False, "Missing email or password")
    
    if User.query.filter_by(email=data["email"]).first():
        return response(False, "User already exists")
    
    hashed_password = generate_password_hash(data["password"])
    new_user = User(email=data["email"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return response(True, "User registered successfully")

# Get Courses
@routes_bp.route("/courses", methods=["GET"])
@jwt_required()
def get_courses():
    courses = Course.query.all()
    return response(True, "Courses fetched", [course.serialize() for course in courses])

# Enroll in a Course
@routes_bp.route("/enroll", methods=["POST"])
@jwt_required()
def enroll_course():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data or "course_id" not in data:
        return response(False, "Missing course ID")
    
    course = Course.query.get(data["course_id"])
    if not course:
        return response(False, "Course not found")
    
    existing_enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course.id).first()
    if existing_enrollment:
        return response(False, "Already enrolled in this course")
    
    enrollment = Enrollment(user_id=user_id, course_id=course.id)
    db.session.add(enrollment)
    db.session.commit()
    return response(True, "Enrollment successful")

# Global Error Handling
@routes_bp.errorhandler(Exception)
def handle_exception(e):
    return response(False, "An error occurred: " + str(e))
