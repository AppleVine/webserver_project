from flask_jwt_extended import get_current_user, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from enum import Enum
from functools import wraps
from app import jwt
from model.user import User


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """ callback for fetching authenticated user from db """
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()


def check_access(role):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            verify_jwt_in_request()
            current_user: User = get_current_user()
            if current_user.role not in role:
                raise NoAuthorizationError("Role is not allowed.")
            return f(*args, **kwargs)
        return decorator_function
    return decorator


def check_id(id):
    verify_jwt_in_request()
    current_user: User = get_current_user()
    user = User.query.get(id)
    if user.id != current_user.id:
        return False
    else:
        return True


def check_access_boolean(role):
    verify_jwt_in_request()
    current_user: User = get_current_user()
    if current_user.role not in role:
        return False
    else:
        return True