from flask import Blueprint, request, jsonify
from models import db, User, Course, Enrollment
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from auth_utils import role_required
from sqlalchemy import and_
from werkzeug.security import check_password_hash

routes_bp = Blueprint("routes_bp", __name__)

@routes_bp.route("/")
def home():
    return jsonify({"message": "Welcome to the Student Course Registration System!"})


@routes_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        # FIX: Include role in the token payload
        access_token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify({
            'token': access_token,
            'role': user.role,
            'user_id': user.id
        }), 200

    return jsonify({'error': 'Invalid credentials'}), 401



@routes_bp.route('/courses', methods=['GET'])
@jwt_required()
def get_courses():
    courses = Course.query.all()
    return jsonify([{ 'id': course.id, 'name': course.name, 'description': course.description, 'prerequisite_id': course.prerequisite_id } for course in courses]), 200

@routes_bp.route('/add_student', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = generate_password_hash(data.get('password'))
    role = 'student'

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    new_student = User(name=name, email=email, password=password, role=role)
    db.session.add(new_student)
    db.session.commit()

    return jsonify({'message': 'Student added successfully'}), 201

@routes_bp.route('/students', methods=['GET'])
def get_students():
    students = User.query.filter_by(role='student').all()
    return jsonify([{ 'id': s.id, 'name': s.name, 'email': s.email } for s in students]), 200


@routes_bp.route('/add_course', methods=['POST'])
@jwt_required()
def add_course():
    user = get_jwt_identity()  # FIX: Fetch user data from JWT token
    if user["role"] != 'admin':
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    prerequisite_id = data.get("prerequisite_id")

    if not name:
        return jsonify({"error": "Course name is required"}), 400

    new_course = Course(name=name, description=description, prerequisite_id=prerequisite_id)
    db.session.add(new_course)
    db.session.commit()

    return jsonify({"message": "Course added successfully!"}), 201


@routes_bp.route('/enroll', methods=['POST'])
@jwt_required()
def enroll():
    print("\n===== /enroll REQUEST RECEIVED =====")  # Debugging

    try:
        student = get_jwt_identity()
        print("Decoded JWT:", student)  # Debugging

        if not isinstance(student, dict):
            print("❌ ERROR: JWT identity is not a dictionary!", student)
            return jsonify({"error": "Invalid JWT format"}), 401

        student_id = student.get("id")
        print("Extracted student_id:", student_id)

        if student_id is None:
            print("❌ ERROR: JWT does not contain 'id'")
            return jsonify({"error": "Invalid JWT: No student ID found"}), 401

        return jsonify({"message": "JWT Verified Successfully!", "student_id": student_id}), 200

    except Exception as e:
        print("🚨 ERROR:", str(e))
        return jsonify({"error": "An unexpected error occurred"}), 500



@routes_bp.route('/debug', methods=['POST'])
def debug_test():
    print("\n===== DEBUG TEST ROUTE RECEIVED =====")
    print("Received Headers:", request.headers)
    print("Content-Type:", request.content_type)
    print("Raw Data:", request.data.decode('utf-8'))
    print("JSON Data:", request.get_json(silent=True))
    
    return jsonify({"message": "Debugging successful!"}), 200

