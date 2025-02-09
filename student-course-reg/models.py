from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User Table (Students & Admins)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student' or 'admin'

# Course Table
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(200), nullable=False)
    course_code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

# Enrollment Table (Many-to-Many: Users & Courses)
class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')
