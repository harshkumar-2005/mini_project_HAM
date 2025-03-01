import os
from flask import Flask, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes import routes_bp
from models import db
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, exceptions

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


@app.errorhandler(exceptions.NoAuthorizationError)
def handle_auth_error(e):
    print("🚨 JWT Authorization Error:", str(e))
    return jsonify({"error": "Missing or invalid JWT token"}), 401

@app.errorhandler(exceptions.JWTDecodeError)
def handle_jwt_decode_error(e):
    print("🚨 JWT Decode Error:", str(e))
    return jsonify({"error": "Invalid JWT format"}), 401



@app.before_request
def log_jwt():
    try:
        verify_jwt_in_request()
        print("✅ JWT Verified:", get_jwt_identity())  # Debugging
    except exceptions.NoAuthorizationError as e:
        print("🚨 JWT Authorization Error:", str(e))
    except exceptions.JWTDecodeError as e:
        print("🚨 JWT Decode Error:", str(e))



# Run Flask App
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000, threaded=False)