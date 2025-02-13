from flask import Blueprint, request, jsonify
from models import db, User, Course, Enrollment
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
from auth_utils import role_required

#  Change Blueprint name from "student_routes" to "routes_bp"
routes_bp = Blueprint("student_routes_bp", __name__)  # Unique name

@routes_bp.route("/")
def home():
    return jsonify({"message": "Welcome to the Student Course Registration System!"})

# Admin-only route
@routes_bp.route("/admin_only", methods=["GET"])
@jwt_required()
@role_required("admin")
def admin_dashboard():
    return jsonify({"message": "Welcome Admin!"})


#  Add Student (with Password Hashing)
@routes_bp.route("/add_student", methods=["POST"])
def add_student():
    data = request.get_json()
    existing_student = User.query.filter_by(email=data["email"]).first()
    
    if existing_student:
        return jsonify({"error": "Email already exists. Please use a different email."}), 400

    try:
        hashed_password = generate_password_hash(data["password"])  #  Hash Password
        new_student = User(name=data["name"], email=data["email"], password=hashed_password, role="student")
        db.session.add(new_student)
        db.session.commit()
        return jsonify({"message": "Student added successfully!"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error. Email must be unique!"}), 400


#  Admin can add courses
@routes_bp.route("/add_course", methods=["POST"])
@jwt_required()
@role_required("admin")
def add_course():
    data = request.get_json()
    new_course = Course(name=data["name"], description=data["description"])
    db.session.add(new_course)
    db.session.commit()
    return jsonify({"message": "Course added successfully!"}), 201


#  Student Enrollment Route
@routes_bp.route("/enroll", methods=["POST"])
@jwt_required()
@role_required("student")
def enroll():
    data = request.get_json()
    
    # Validate input
    if "user_id" not in data or "course_id" not in data:
        return jsonify({"error": "Missing user_id or course_id"}), 400

    enrollment = Enrollment(user_id=data["user_id"], course_id=data["course_id"])
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({"message": "Enrollment successful!"}), 201


#  Admin can view all enrollments
@routes_bp.route('/enrollments', methods=['GET'])
@jwt_required()
@role_required("admin")
def get_enrollments():
    enrollments = Enrollment.query.all()
    result = [
        {
            "id": e.id,
            "user_id": e.user_id,
            "user_name": e.user.name,
            "course_id": e.course_id,
            "course_name": e.course.name
        }
        for e in enrollments
    ]
    return jsonify(result), 200


#  Get all courses
@routes_bp.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    result = [{"id": c.id, "name": c.name, "description": c.description} for c in courses]
    return jsonify(result), 200


#  Get all students
@routes_bp.route('/students', methods=['GET'])
def get_students():
    students = User.query.filter(User.role == "student").all()
    result = [{"id": s.id, "name": s.name, "email": s.email} for s in students]
    return jsonify(result), 200


#  Login Route (Corrected with JWT Token Generation)
@routes_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Query user from database
    user = User.query.filter_by(email=username).first()

    #  Validate password
    if user and check_password_hash(user.password, password):
        token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401
