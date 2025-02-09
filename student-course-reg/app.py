from flask import Flask
from models import db
from routes import routes_bp

app = Flask(__name__)

# Configure database URI (if not already configured)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://username:password@localhost/your_database"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Register Blueprint
app.register_blueprint(routes_bp)

if __name__ == "__main__":
    app.run(debug=True)
