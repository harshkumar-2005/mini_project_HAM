from flask import Flask
from models import db  # Import database
from routes import routes_bp  # Import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Import Migrate
from models import db  # Import database
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your_secret_key"  # Change this in production
jwt = JWTManager(app)

#  Database Configuration (Correct connection string format)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%40Harsh1243@localhost/student_course_reg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  Initialize database with app
db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Register the Blueprint
app.register_blueprint(routes_bp)

# Ensure database tables are created (Run this before first use)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

