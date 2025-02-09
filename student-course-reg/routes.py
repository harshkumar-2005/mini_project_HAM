from flask import Blueprint, request, jsonify
from models import db, User, Course, Enrollment

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/")
def home():
    return jsonify({"message": "Welcome to the Student Course Registration System!"})

@routes_bp.route("/add_student", methods=["POST"])
def add_student():
    data = request.get_json()
    new_student = User(name=data["name"], email=data["email"], role="student")
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully!"})

@routes_bp.route("/add_course", methods=["POST"])
def add_course():
    data = request.get_json()
    new_course = Course(name=data["name"], description=data["description"])
    db.session.add(new_course)
    db.session.commit()
    return jsonify({"message": "Course added successfully!"})

@routes_bp.route("/enroll", methods=["POST"])
def enroll():
    data = request.get_json()
    enrollment = Enrollment(student_id=data["student_id"], course_id=data["course_id"])
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({"message": "Enrollment successful!"})
