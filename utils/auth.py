from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

jwt = JWTManager()

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed):
    return check_password_hash(hashed, password)

def create_token(user_id, role):
    from flask_jwt_extended import create_access_token
    return create_access_token(identity={"id": user_id, "role": role})

# Role check decorator
def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            if identity.get("role") != role:
                return {"error": "Unauthorized - Admins only"}, 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
