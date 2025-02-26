import os
from flask import Flask, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes import routes_bp
from models import db

# Initialize Flask App
app = Flask(__name__, static_folder="static")  # Adjusted for Vanilla JS frontend

# Enable CORS for specific frontend origins
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})  # Adjust frontend port if needed

# Database Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your_secret_key")  # Change in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%40Harsh1243@localhost/student_registration_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Register Blueprint (API Routes)
app.register_blueprint(routes_bp)

# Ensure Database Tables Exist
with app.app_context():
    db.create_all()

# Serve Vanilla JS Frontend
@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")


# Health Check Route
@app.route("/health")
def health_check():
    return jsonify({"status": "OK"}), 200

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=False)