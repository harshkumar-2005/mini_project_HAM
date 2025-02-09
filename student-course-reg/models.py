from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User Table (Students & Admins)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Ensure 'name' exists
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student' or 'admin'

# Course Table
class Course(db.Model):
    __tablename__ = 'courses'  # Ensure this matches your actual database table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Ensure this exists
    description = db.Column(db.Text, nullable=True)   # Ensure this exists

    def __init__(self, name, description):
        self.name = name
        self.description = description

# Enrollment Table (Many-to-Many: Users & Courses)
class Enrollment(db.Model):
    __tablename__ = 'enrollments'  # Ensure this matches the actual table name in the database

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)  # This should match the actual table name
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    def __init__(self, student_id, course_id):
        self.student_id = student_id
        self.course_id = course_id

class Student(db.Model):
    __tablename__ = 'students'  # This MUST match the ForeignKey in Enrollment

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

