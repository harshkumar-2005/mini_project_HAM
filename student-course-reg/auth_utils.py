from functools import wraps
from flask import request, jsonify
import jwt

# Secret key for JWT (Make sure it's the same as used in your app)
SECRET_KEY = "your_secret_key"

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return jsonify({"error": "Authorization token is missing"}), 401

            try:
                token = auth_header.split(" ")[1]
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                user_role = decoded_token.get("role")

                if user_role != required_role:
                    return jsonify({"error": "Permission denied"}), 403

            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401

            return f(*args, **kwargs)

        return decorated_function
    return decorator
