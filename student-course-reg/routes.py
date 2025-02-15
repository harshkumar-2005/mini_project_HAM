from flask import Blueprint, request, jsonify
from models import db, User, Course, Enrollment
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
from auth_utils import role_required

#  Define a Unique Blueprint Name
routes_bp = Blueprint("routes_bp", __name__)  # Unique to avoid duplicate registration

@routes_bp.route("/")
def home():
    return jsonify({"message": "Welcome to the Student Course Registration System!"})

#  Admin-only route
@routes_bp.route("/admin_only", methods=["GET"])
@jwt_required()
@role_required("admin")
def admin_dashboard():
    return jsonify({"message": "Welcome Admin!"})

#  Add Student (With Password Hashing)
@routes_bp.route("/add_student", methods=["POST"])
def add_student():
    data = request.get_json()
    existing_student = User.query.filter_by(email=data["email"]).first()
    
    if existing_student:
        return jsonify({"error": "Email already exists. Please use a different email."}), 400

    try:
        hashed_password = generate_password_hash(data["password"])  # Hash Password
        new_student = User(name=data["name"], email=data["email"], password=hashed_password, role="student")
        db.session.add(new_student)
        db.session.commit()
        return jsonify({"message": "Student added successfully!"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error. Email must be unique!"}), 400

#  Admin Can Add Courses
@routes_bp.route("/add_course", methods=["POST"])
@jwt_required()
@role_required("admin")
def add_course():
    data = request.get_json()
    print(" DEBUG: Received Course Data:", data)  # Debugging Output

    if not data:
        return jsonify({"error": "No data received. Make sure you're sending JSON."}), 422

    if "name" not in data or "description" not in data:
        return jsonify({"error": "Missing required fields: name, description"}), 422

    new_course = Course(name=data["name"], description=data["description"])
    db.session.add(new_course)
    db.session.commit()
    return jsonify({"message": "Course added successfully!"}), 201


#  Student Enrollment Route
@routes_bp.route('/enroll', methods=['POST'])
def enroll_student():
    data = request.get_json()
    print(" DEBUG: Received Enrollment Data:", data)  #  Debugging

    user_id = data.get("user_id")
    course_id = data.get("course_id")
    subject = data.get("subject", None)  # Default to None if not provided

    if not user_id or not course_id:
        return jsonify({"msg": "Invalid input. Ensure user_id and course_id are provided."}), 422

    try:
        #  Only include subject if it's provided
        new_enrollment = Enrollment(user_id=user_id, course_id=course_id, subject=subject if subject else None)
        db.session.add(new_enrollment)
        db.session.commit()

        return jsonify({"msg": "Enrollment successful!"}), 201

    except Exception as e:
        print(" Error:", str(e))  # Debugging Output
        return jsonify({"msg": "An error occurred during enrollment", "error": str(e)}), 500

#  Admin Can View All Enrollments
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

#  Get All Courses
@routes_bp.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    result = [{"id": c.id, "name": c.name, "description": c.description} for c in courses]
    return jsonify(result), 200

#  Get All Students
@routes_bp.route('/students', methods=['GET'])
def get_students():
    students = User.query.filter(User.role == "student").all()
    result = [{"id": s.id, "name": s.name, "email": s.email} for s in students]
    return jsonify(result), 200

#  Login Route (JWT Token Generation)
@routes_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    print(f" DEBUG: Stored Hashed Password: {user.password}")  # Debugging

    if not check_password_hash(user.password, password):  # Check password
        print(" Password does not match!")
        return jsonify({"error": "Incorrect password"}), 401

    print(" Password matches!")  # Debugging
    token = create_access_token(identity={"id": user.id, "role": user.role})  # Generate JWT
    return jsonify({"token": token, "role": user.role}), 200
