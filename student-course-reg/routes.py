from flask import Blueprint, request, jsonify
from models import db, User, Course, Enrollment
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from auth_utils import role_required

routes_bp = Blueprint("routes_bp", __name__)

@routes_bp.route("/")
def home():
    return jsonify({"message": "Welcome to the Student Course Registration System!"})

# Student Enrollment with Prerequisite Check
@routes_bp.route('/enroll', methods=['POST'])
@jwt_required()
def enroll():
    student_id = get_jwt_identity()
    course_id = request.json.get('course_id')
    course = Course.query.get(course_id)
    
    if course is None:
        return jsonify({'error': 'Course not found'}), 404
    
    if course.prerequisite_id:
        prerequisite = Course.query.get(course.prerequisite_id)
        if not Enrollment.query.filter_by(student_id=student_id, course_id=prerequisite.id).first():
            return jsonify({'error': 'Prerequisite not met'}), 400
    
    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({'message': 'Enrolled successfully'}), 201

# Bulk Enrollment
@routes_bp.route('/bulk-enroll', methods=['POST'])
@jwt_required()
def bulk_enroll():
    student_id = get_jwt_identity()
    course_ids = request.json.get('course_ids', [])
    
    enrolled_courses = []
    failed_courses = []
    
    for course_id in course_ids:
        course = Course.query.get(course_id)
        if not course:
            failed_courses.append({'course_id': course_id, 'error': 'Course not found'})
            continue
        
        if course.prerequisite_id:
            prerequisite = Course.query.get(course.prerequisite_id)
            if not Enrollment.query.filter_by(student_id=student_id, course_id=prerequisite.id).first():
                failed_courses.append({'course_id': course_id, 'error': 'Prerequisite not met'})
                continue
        
        enrollment = Enrollment(student_id=student_id, course_id=course_id)
        db.session.add(enrollment)
        enrolled_courses.append(course_id)
    
    db.session.commit()
    return jsonify({'enrolled': enrolled_courses, 'failed': failed_courses}), 200
