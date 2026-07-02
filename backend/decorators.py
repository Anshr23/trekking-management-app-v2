from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from extensions import db
from models import User


def role_required(required_role):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            user_id = int(get_jwt_identity())
            user = db.session.get(User, user_id)

            if user is None:
                return jsonify({
                    "message": "User not found"
                }), 404

            if not user.is_active:
                return jsonify({
                    "message": "Your account is inactive"
                }), 403

            if user.is_blacklisted:
                return jsonify({
                    "message": "Your account has been blacklisted"
                }), 403

            if user.role != required_role:
                return jsonify({
                    "message": "You do not have permission to access this resource"
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator


admin_required = role_required("admin")
staff_required = role_required("staff")
trekker_required = role_required("trekker")