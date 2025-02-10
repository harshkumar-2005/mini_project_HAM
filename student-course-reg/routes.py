from flask import Blueprint, request, jsonify
from models import db, User, Course, Enrollment
from sqlalchemy.exc import IntegrityError

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/")
def home():
    return jsonify({"message": "Welcome to the Student Course Registration System!"})

@routes_bp.route("/add_student", methods=["POST"])
def add_student():
    data = request.get_json()
    print("Received data:", data)  # Debugging output
    # Check if a user with the same email already exists
    existing_student = User.query.filter_by(email=data["email"]).first()
    
    if existing_student:
        return jsonify({"error": "Email already exists. Please use a different email."}), 400

    try:
        new_student = User(name=data["name"], email=data["email"], role="student")
        db.session.add(new_student)
        db.session.commit()
        return jsonify({"message": "Student added successfully!"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error. Email must be unique!"}), 400


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
    enrollment = Enrollment(user_id=data["user_id"], course_id=data["course_id"])  # FIXED
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({"message": "Enrollment successful!"})


@routes_bp.route('/enrollments', methods=['GET'])
def get_enrollments():
    enrollments = Enrollment.query.all()
    result = [
        {
            "id": e.id,
            "user_id": e.user_id,  # FIXED
            "user_name": e.user.name,  # FIXED
            "course_id": e.course_id,
            "course_name": e.course.name
        }
        for e in enrollments
    ]
    return jsonify(result), 200




@routes_bp.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()  # Fetch all courses from the database
    result = [{"id": c.id, "name": c.name, "description": c.description} for c in courses]
    return jsonify(result), 200


@routes_bp.route('/students', methods=['GET'])
def get_students():
    # Ensure the role column exists
    students = User.query.filter(User.role == "student").all()
    result = [{"id": s.id, "name": s.name, "email": s.email} for s in students]
    return jsonify(result), 200



