import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes import routes_bp
from models import db

#  Initialize Flask App
app = Flask(__name__, static_folder="frontend/build")

#  Enable CORS (Cross-Origin Resource Sharing)
CORS(app)

#  Database Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your_secret_key")  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%40Harsh1243@localhost/student_registration_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  Initialize Extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

#  Register Blueprint (API Routes)
app.register_blueprint(routes_bp)

#  Ensure Database Tables Exist
with app.app_context():
    db.create_all()

#  Serve React Frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

#  Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
