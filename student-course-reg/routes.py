from flask import Blueprint, request, jsonify
from models import db, User, Course, Enrollment
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from auth_utils import role_required
from sqlalchemy import and_

routes_bp = Blueprint("routes_bp", __name__)

@routes_bp.route("/")
def home():
    return jsonify({"message": "Welcome to the Student Course Registration System!"})

@routes_bp.route('/enroll', methods=['POST'])
@jwt_required()
def enroll():
    user_id = get_jwt_identity()
    course_id = request.json.get('course_id')
    
    # Check if already enrolled
    existing_enrollment = Enrollment.query.filter_by(
        user_id=user_id, 
        course_id=course_id
    ).first()
    
    if existing_enrollment:
        return jsonify({'error': 'Already enrolled in this course'}), 400
    
    # Get course and check prerequisites in a single query
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    if course.prerequisite_id:
        has_prerequisite = Enrollment.query.filter_by(
            user_id=user_id, 
            course_id=course.prerequisite_id
        ).scalar() is not None
        
        if not has_prerequisite:
            return jsonify({'error': 'Prerequisite not met'}), 400
    
    try:
        enrollment = Enrollment(user_id=user_id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        return jsonify({'message': 'Enrolled successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Enrollment failed'}), 400

@routes_bp.route('/bulk-enroll', methods=['POST'])
@jwt_required()
def bulk_enroll():
    user_id = get_jwt_identity()
    course_ids = request.json.get('course_ids', [])
    
    if not course_ids:
        return jsonify({'error': 'No courses provided'}), 400
    
    # Get all requested courses in a single query
    courses = Course.query.filter(Course.id.in_(course_ids)).all()
    course_dict = {course.id: course for course in courses}
    
    # Get existing enrollments in a single query
    existing_enrollments = set(
        e[0] for e in db.session.query(Enrollment.course_id).filter(
            and_(
                Enrollment.user_id == user_id,
                Enrollment.course_id.in_(course_ids)
            )
        ).all()
    )
    
    # Get all prerequisites in a single query
    prereq_courses = {c.id for c in courses if c.prerequisite_id}
    prereq_enrollments = set(
        e[0] for e in db.session.query(Enrollment.course_id).filter(
            and_(
                Enrollment.user_id == user_id,
                Enrollment.course_id.in_([c.prerequisite_id for c in courses if c.prerequisite_id])
            )
        ).all()
    )
    
    enrolled_courses = []
    failed_courses = []
    enrollments_to_add = []
    
    for course_id in course_ids:
        if course_id in existing_enrollments:
            failed_courses.append({'course_id': course_id, 'error': 'Already enrolled'})
            continue
            
        course = course_dict.get(course_id)
        if not course:
            failed_courses.append({'course_id': course_id, 'error': 'Course not found'})
            continue
        
        if course.prerequisite_id and course.prerequisite_id not in prereq_enrollments:
            failed_courses.append({'course_id': course_id, 'error': 'Prerequisite not met'})
            continue
        
        enrollments_to_add.append(
            Enrollment(user_id=user_id, course_id=course_id)
        )
        enrolled_courses.append(course_id)
    
    try:
        if enrollments_to_add:
            db.session.bulk_save_objects(enrollments_to_add)
            db.session.commit()
        return jsonify({
            'enrolled': enrolled_courses, 
            'failed': failed_courses
        }), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Bulk enrollment failed'}), 400

        