from datetime import datetime

from flask import Blueprint, jsonify, request

from decorators import admin_required
from extensions import db
from models import User, StaffProfile, Trek, Booking


admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.route("/dashboard", methods=["GET"])
@admin_required
def get_dashboard():
    total_treks = Trek.query.count()

    total_users = User.query.filter_by(role="trekker").count()

    total_staff = User.query.filter_by(role="staff").count()

    total_bookings = Booking.query.count()

    active_treks = Trek.query.filter(
        Trek.status.in_(["Open", "Ongoing"])
    ).count()

    completed_treks = Trek.query.filter_by(
        status="Completed"
    ).count()

    return jsonify({
        "total_treks": total_treks,
        "total_users": total_users,
        "total_staff": total_staff,
        "total_bookings": total_bookings,
        "active_treks": active_treks,
        "completed_treks": completed_treks
    }), 200


@admin_bp.route("/treks", methods=["GET"])
@admin_required
def get_all_treks():
    search = request.args.get("search", "").strip()
    difficulty = request.args.get("difficulty", "").strip()
    status = request.args.get("status", "").strip()

    query = Trek.query

    if search:
        query = query.filter(
            db.or_(
                Trek.name.ilike(f"%{search}%"),
                Trek.location.ilike(f"%{search}%")
            )
        )

    if difficulty:
        query = query.filter_by(difficulty=difficulty)

    if status:
        query = query.filter_by(status=status)

    treks = query.order_by(Trek.created_at.desc()).all()

    return jsonify({
        "treks": [trek.to_dict() for trek in treks]
    }), 200


@admin_bp.route("/treks/<int:trek_id>", methods=["GET"])
@admin_required
def get_trek(trek_id):
    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return jsonify({
            "message": "Trek not found"
        }), 404

    return jsonify({
        "trek": trek.to_dict()
    }), 200


@admin_bp.route("/treks", methods=["POST"])
@admin_required
def create_trek():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data provided"
        }), 400

    required_fields = [
        "name",
        "location",
        "difficulty",
        "duration",
        "total_slots",
        "start_date",
        "end_date"
    ]

    for field in required_fields:
        if data.get(field) in (None, ""):
            return jsonify({
                "message": f"{field.replace('_', ' ').title()} is required"
            }), 400

    difficulty = str(data["difficulty"]).strip().title()

    if difficulty not in ["Easy", "Moderate", "Hard"]:
        return jsonify({
            "message": "Difficulty must be Easy, Moderate or Hard"
        }), 400

    try:
        duration = int(data["duration"])
        total_slots = int(data["total_slots"])
        price = float(data.get("price", 0))
        altitude = (
            int(data["altitude"])
            if data.get("altitude") not in (None, "")
            else None
        )

        start_date = datetime.strptime(
            data["start_date"],
            "%Y-%m-%d"
        ).date()

        end_date = datetime.strptime(
            data["end_date"],
            "%Y-%m-%d"
        ).date()

    except (ValueError, TypeError):
        return jsonify({
            "message": "Invalid numeric value or date format"
        }), 400

    if duration <= 0:
        return jsonify({
            "message": "Duration must be greater than zero"
        }), 400

    if total_slots <= 0:
        return jsonify({
            "message": "Total slots must be greater than zero"
        }), 400

    if price < 0:
        return jsonify({
            "message": "Price cannot be negative"
        }), 400

    if end_date < start_date:
        return jsonify({
            "message": "End date cannot be before start date"
        }), 400

    trek = Trek(
        name=data["name"].strip(),
        location=data["location"].strip(),
        description=data.get("description", "").strip(),
        difficulty=difficulty,
        duration=duration,
        total_slots=total_slots,
        available_slots=total_slots,
        status="Pending",
        start_date=start_date,
        end_date=end_date,
        price=price,
        altitude=altitude,
        image_url=data.get("image_url", "").strip()
    )

    db.session.add(trek)
    db.session.commit()

    return jsonify({
        "message": "Trek created successfully",
        "trek": trek.to_dict()
    }), 201


@admin_bp.route("/treks/<int:trek_id>", methods=["PUT"])
@admin_required
def update_trek(trek_id):
    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return jsonify({
            "message": "Trek not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data provided"
        }), 400

    if "name" in data:
        name = str(data["name"]).strip()

        if not name:
            return jsonify({
                "message": "Trek name cannot be empty"
            }), 400

        trek.name = name

    if "location" in data:
        location = str(data["location"]).strip()

        if not location:
            return jsonify({
                "message": "Location cannot be empty"
            }), 400

        trek.location = location

    if "description" in data:
        trek.description = str(data["description"]).strip()

    if "difficulty" in data:
        difficulty = str(data["difficulty"]).strip().title()

        if difficulty not in ["Easy", "Moderate", "Hard"]:
            return jsonify({
                "message": "Difficulty must be Easy, Moderate or Hard"
            }), 400

        trek.difficulty = difficulty

    if "duration" in data:
        try:
            duration = int(data["duration"])
        except (ValueError, TypeError):
            return jsonify({
                "message": "Duration must be a valid number"
            }), 400

        if duration <= 0:
            return jsonify({
                "message": "Duration must be greater than zero"
            }), 400

        trek.duration = duration

    if "total_slots" in data:
        try:
            new_total_slots = int(data["total_slots"])
        except (ValueError, TypeError):
            return jsonify({
                "message": "Total slots must be a valid number"
            }), 400

        booked_slots = trek.total_slots - trek.available_slots

        if new_total_slots < booked_slots:
            return jsonify({
                "message": (
                    "Total slots cannot be less than the number "
                    "of already booked slots"
                )
            }), 400

        trek.total_slots = new_total_slots
        trek.available_slots = new_total_slots - booked_slots

    if "status" in data:
        allowed_statuses = [
            "Pending",
            "Approved",
            "Open",
            "Closed",
            "Ongoing",
            "Completed"
        ]

        status = str(data["status"]).strip().title()

        if status not in allowed_statuses:
            return jsonify({
                "message": "Invalid trek status"
            }), 400

        trek.status = status

    if "start_date" in data:
        try:
            trek.start_date = datetime.strptime(
                data["start_date"],
                "%Y-%m-%d"
            ).date()
        except (ValueError, TypeError):
            return jsonify({
                "message": "Invalid start date format"
            }), 400

    if "end_date" in data:
        try:
            trek.end_date = datetime.strptime(
                data["end_date"],
                "%Y-%m-%d"
            ).date()
        except (ValueError, TypeError):
            return jsonify({
                "message": "Invalid end date format"
            }), 400

    if trek.end_date < trek.start_date:
        return jsonify({
            "message": "End date cannot be before start date"
        }), 400

    if "price" in data:
        try:
            price = float(data["price"])
        except (ValueError, TypeError):
            return jsonify({
                "message": "Price must be a valid number"
            }), 400

        if price < 0:
            return jsonify({
                "message": "Price cannot be negative"
            }), 400

        trek.price = price

    if "altitude" in data:
        if data["altitude"] in (None, ""):
            trek.altitude = None
        else:
            try:
                trek.altitude = int(data["altitude"])
            except (ValueError, TypeError):
                return jsonify({
                    "message": "Altitude must be a valid number"
                }), 400

    if "image_url" in data:
        trek.image_url = str(data["image_url"]).strip()

    db.session.commit()

    return jsonify({
        "message": "Trek updated successfully",
        "trek": trek.to_dict()
    }), 200


@admin_bp.route("/treks/<int:trek_id>", methods=["DELETE"])
@admin_required
def delete_trek(trek_id):
    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return jsonify({
            "message": "Trek not found"
        }), 404

    if trek.bookings:
        return jsonify({
            "message": "Cannot delete a trek that has booking records"
        }), 400

    db.session.delete(trek)
    db.session.commit()

    return jsonify({
        "message": "Trek deleted successfully"
    }), 200


@admin_bp.route("/staff", methods=["GET"])
@admin_required
def get_all_staff():
    search = request.args.get("search", "").strip()

    query = User.query.filter_by(role="staff")

    if search:
        query = query.filter(
            db.or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )

    staff_members = query.order_by(User.created_at.desc()).all()

    result = []

    for staff in staff_members:
        staff_data = staff.to_dict()

        if staff.staff_profile:
            staff_data["profile"] = staff.staff_profile.to_dict()
        else:
            staff_data["profile"] = None

        staff_data["assigned_treks"] = [
            {
                "id": trek.id,
                "name": trek.name,
                "status": trek.status
            }
            for trek in staff.assigned_treks
        ]

        result.append(staff_data)

    return jsonify({
        "staff": result
    }), 200


@admin_bp.route("/staff", methods=["POST"])
@admin_required
def create_staff():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data provided"
        }), 400

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    phone = str(data.get("phone", "")).strip()

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

    try:
        experience_years = int(data.get("experience_years", 0))
    except (ValueError, TypeError):
        return jsonify({
            "message": "Experience must be a valid number"
        }), 400

    if experience_years < 0:
        return jsonify({
            "message": "Experience cannot be negative"
        }), 400

    staff = User(
        name=name,
        email=email,
        phone=phone,
        role="staff"
    )

    staff.set_password(password)

    db.session.add(staff)
    db.session.flush()

    profile = StaffProfile(
        user_id=staff.id,
        experience_years=experience_years,
        specialization=str(
            data.get("specialization", "")
        ).strip(),
        emergency_contact=str(
            data.get("emergency_contact", "")
        ).strip(),
        bio=str(data.get("bio", "")).strip(),
        status="Active"
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({
        "message": "Trek staff created successfully",
        "staff": staff.to_dict(),
        "profile": profile.to_dict()
    }), 201


@admin_bp.route("/staff/<int:staff_id>", methods=["PUT"])
@admin_required
def update_staff(staff_id):
    staff = db.session.get(User, staff_id)

    if staff is None or staff.role != "staff":
        return jsonify({
            "message": "Staff member not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data provided"
        }), 400

    if "name" in data:
        name = str(data["name"]).strip()

        if not name:
            return jsonify({
                "message": "Name cannot be empty"
            }), 400

        staff.name = name

    if "phone" in data:
        staff.phone = str(data["phone"]).strip()

    if "experience_years" in data:
        try:
            experience = int(data["experience_years"])
        except (ValueError, TypeError):
            return jsonify({
                "message": "Experience must be a valid number"
            }), 400

        if experience < 0:
            return jsonify({
                "message": "Experience cannot be negative"
            }), 400

        staff.staff_profile.experience_years = experience

    if "specialization" in data:
        staff.staff_profile.specialization = str(
            data["specialization"]
        ).strip()

    if "emergency_contact" in data:
        staff.staff_profile.emergency_contact = str(
            data["emergency_contact"]
        ).strip()

    if "bio" in data:
        staff.staff_profile.bio = str(data["bio"]).strip()

    db.session.commit()

    return jsonify({
        "message": "Staff details updated successfully"
    }), 200



@admin_bp.route(
    "/treks/<int:trek_id>/assign-staff",
    methods=["PUT"]
)
@admin_required
def assign_staff_to_trek(trek_id):
    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return jsonify({
            "message": "Trek not found"
        }), 404

    data = request.get_json()

    if not data or data.get("staff_id") is None:
        return jsonify({
            "message": "Staff ID is required"
        }), 400

    staff = db.session.get(User, data["staff_id"])

    if staff is None or staff.role != "staff":
        return jsonify({
            "message": "Valid trek staff not found"
        }), 404

    if not staff.is_active or staff.is_blacklisted:
        return jsonify({
            "message": "Cannot assign inactive or blacklisted staff"
        }), 400

    trek.assigned_staff_id = staff.id

    if trek.status == "Pending":
        trek.status = "Approved"

    db.session.commit()

    return jsonify({
        "message": "Staff assigned to trek successfully",
        "trek": trek.to_dict()
    }), 200


@admin_bp.route("/users", methods=["GET"])
@admin_required
def get_all_users():
    search = request.args.get("search", "").strip()

    query = User.query.filter_by(role="trekker")

    if search:
        query = query.filter(
            db.or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )

    users = query.order_by(User.created_at.desc()).all()

    return jsonify({
        "users": [user.to_dict() for user in users]
    }), 200


@admin_bp.route(
    "/users/<int:user_id>/toggle-active",
    methods=["PUT"]
)
@admin_required
def toggle_user_active_status(user_id):
    user = db.session.get(User, user_id)

    if user is None or user.role == "admin":
        return jsonify({
            "message": "User not found"
        }), 404

    user.is_active = not user.is_active

    db.session.commit()

    return jsonify({
        "message": (
            "Account activated successfully"
            if user.is_active
            else "Account deactivated successfully"
        ),
        "user": user.to_dict()
    }), 200


@admin_bp.route(
    "/users/<int:user_id>/toggle-blacklist",
    methods=["PUT"]
)
@admin_required
def toggle_user_blacklist(user_id):
    user = db.session.get(User, user_id)

    if user is None or user.role == "admin":
        return jsonify({
            "message": "User not found"
        }), 404

    user.is_blacklisted = not user.is_blacklisted

    db.session.commit()

    return jsonify({
        "message": (
            "User blacklisted successfully"
            if user.is_blacklisted
            else "User removed from blacklist successfully"
        ),
        "user": user.to_dict()
    }), 200


@admin_bp.route("/bookings", methods=["GET"])
@admin_required
def get_all_bookings():
    status = request.args.get("status", "").strip()

    query = Booking.query

    if status:
        query = query.filter_by(status=status)

    bookings = query.order_by(
        Booking.booking_date.desc()
    ).all()

    return jsonify({
        "bookings": [
            booking.to_dict()
            for booking in bookings
        ]
    }), 200

