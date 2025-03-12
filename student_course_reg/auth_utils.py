from functools import wraps
from flask import request, jsonify
import jwt

# Secret key for JWT (Ensure this matches the key in your app config)
SECRET_KEY = "your_secret_key"

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            
            if not auth_header:
                return jsonify({"error": "Authorization token is missing"}), 401
            
            parts = auth_header.split(" ")
            if len(parts) != 2 or parts[0] != "Bearer":
                return jsonify({"error": "Invalid token format"}), 401
            
            token = parts[1]
            try:
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                
                # Extract user role correctly
                user_role = decoded_token.get("role")  # Ensure 'role' is set in JWT payload
                if not user_role:
                    return jsonify({"error": "Role not found in token"}), 403
                
                if user_role != required_role:
                    return jsonify({"error": "Permission denied"}), 403
                
                return f(*args, **kwargs)
            
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401
        
        return decorated_function
    return decorator
