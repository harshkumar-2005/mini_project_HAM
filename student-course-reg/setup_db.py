from app import app, db
from models import User, Course
from werkzeug.security import generate_password_hash

def setup_database():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        print("Database and tables created successfully!")

        # Ensure a default admin user exists
        if not User.query.filter_by(role="admin").first():
            default_admin = User(
                name="Admin User",
                email="admin@example.com",
                password=generate_password_hash("adminpassword"),  # Securely hash the password
                role="admin"
            )
            db.session.add(default_admin)
            db.session.commit()
            print("Added a default admin user.")

        # Ensure at least one student exists
        if not User.query.filter_by(role="student").first():
            default_student = User(
                name="Harsh",
                email="harsh@example.com",
                password=generate_password_hash("password123"),  # Hash password
                role="student"
            )
            db.session.add(default_student)
            db.session.commit()
            print("Added a default student.")

        # Ensure at least one course exists
        if not Course.query.first():
            default_course = Course(
                name="Python Basics",
                description="Introduction to Python Programming."
            )
            db.session.add(default_course)
            db.session.commit()
            print("Added a default course.")

if __name__ == "__main__":
    setup_database()
