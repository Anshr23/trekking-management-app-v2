from flask import Blueprint, request, jsonify
#from decorators import admin_required, staff_required, trekker_required
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required
)

from extensions import db
from models import User


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    phone = data.get("phone", "").strip()

    if not name or not email or not password:
        return jsonify({
            "message": "Name, email and password are required"
        }), 400

    if len(password) < 6:
        return jsonify({
            "message": "Password must be at least 6 characters long"
        }), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "message": "An account with this email already exists"
        }), 409

    user = User(
        name=name,
        email=email,
        phone=phone,
        role="trekker"
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Registration successful",
        "user": user.to_dict()
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    if not user.is_active:
        return jsonify({
            "message": "Your account is inactive"
        }), 403

    if user.is_blacklisted:
        return jsonify({
            "message": "Your account has been blacklisted"
        }), 403

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
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

    return jsonify({
        "user": user.to_dict()
    }), 200



#temp routes for testing 
# @auth_bp.route("/test-admin", methods=["GET"])
# @admin_required
# def test_admin_access():
#     return jsonify({
#         "message": "Admin access granted"
#     }), 200

# @auth_bp.route("/test-staff", methods=["GET"])
# @staff_required
# def test_staff_access():
#     return jsonify({
#         "message": "Staff access granted"
#     }), 200

# @auth_bp.route("/test-trekker", methods=["GET"])
# @trekker_required
# def test_trekker_access():
#     return jsonify({
#         "message": "Trekker access granted"
#     }), 200




