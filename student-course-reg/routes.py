from flask import Blueprint, request, jsonify
from models import db, User, Course, Enrollment

# Create a Blueprint
routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/")
def home():
    return jsonify({"message": "Welcome to the Student Course Registration System!"})

# ---------------- Student Routes ----------------
@routes_bp.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    new_student = User(name=data["name"], email=data["email"], role="student")
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully!"})

@routes_bp.route("/students", methods=["GET"])
def get_students():
    students = User.query.filter_by(role="student").all()
    return jsonify([{"id": s.id, "name": s.name, "email": s.email} for s in students])

# ---------------- Course Routes ----------------
@routes_bp.route("/courses", methods=["POST"])
def add_course():
    data = request.get_json()
    new_course = Course(name=data["name"], description=data["description"])
    db.session.add(new_course)
    db.session.commit()
    return jsonify({"message": "Course added successfully!"})

@routes_bp.route("/courses", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return jsonify([{"id": c.id, "name": c.name, "description": c.description} for c in courses])

# ---------------- Enrollment Routes ----------------
@routes_bp.route("/enroll", methods=["POST"])
def enroll():
    data = request.get_json()
    enrollment = Enrollment(student_id=data["student_id"], course_id=data["course_id"])
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({"message": "Enrollment successful!"})

@routes_bp.route("/enrollments", methods=["GET"])
def get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify([{"id": e.id, "student_id": e.student_id, "course_id": e.course_id} for e in enrollments])
