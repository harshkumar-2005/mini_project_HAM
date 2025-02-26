from flask_sqlalchemy import SQLAlchemy

# Define the db instance once and use it in app.py
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    
    # Add validation for role values
    VALID_ROLES = ['student', 'admin']
    
    def __repr__(self):
        return f'<User {self.name}>'

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    
    # Add prerequisite relationship
    prerequisite_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    prerequisite = db.relationship('Course', remote_side=[id], backref='dependent_courses')
    
    def __repr__(self):
        return f'<Course {self.name}>'

class Enrollment(db.Model):
    __tablename__ = "enrollments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=True)

    # Define relationships
    user = db.relationship('User', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')
    
    def __repr__(self):
        return f'<Enrollment {self.user_id}:{self.course_id}>'
    