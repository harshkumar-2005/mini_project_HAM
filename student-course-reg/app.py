from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from routes import routes_bp
from models import db  # ✅ Import the existing db instance
import os

app = Flask(__name__)

# ✅ Database Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your_secret_key")  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%40Harsh1243@localhost/student_registration_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Initialize database
db.init_app(app)  # ✅ Ensure the app is registered with SQLAlchemy
migrate = Migrate(app, db)
jwt = JWTManager(app)

# ✅ Register Blueprint
app.register_blueprint(routes_bp)

# ✅ Ensure database tables exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
