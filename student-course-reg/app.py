import os
from datetime import timedelta
from flask import Flask, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from routes import routes_bp
from models import db
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="static")

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)


# Initialize Flask App
app = Flask(__name__, static_folder="static")

# Enable CORS for all origins (Temporary fix)
CORS(app)

# Database Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:%40Harsh1243@localhost/student_registration_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# Initialize Extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Register Blueprint (API Routes)
app.register_blueprint(routes_bp)

# Ensure Database Tables Exist
with app.app_context():
    db.create_all()

# Token Refresh Route
@app.route("/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    new_token = create_access_token(identity=identity)
    return jsonify({"token": new_token}), 200

# Serve Frontend
@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

# Health Check
@app.route("/health")
def health_check():
    return jsonify({"status": "OK"}), 200

# Run Flask App
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000, threaded=False)
