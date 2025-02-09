from flask import Flask
from models import db
from routes import routes_bp  # Make sure you are importing routes_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://username:password@localhost/db_name"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(routes_bp)  # Correct way to register blueprint

if __name__ == "__main__":
    app.run(debug=True)
