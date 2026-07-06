from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity

from decorators import role_required
from extensions import db
from models import User, Trek, Booking


trekker_bp = Blueprint(
    "trekker",
    __name__,
    url_prefix="/api/trekker"
)


def get_current_trekker():
    user_id = int(get_jwt_identity())
    return db.session.get(User, user_id)


@trekker_bp.route("/dashboard", methods=["GET"])
@role_required("trekker")
def get_dashboard():
    user = get_current_trekker()

    available_treks = Trek.query.filter_by(
        status="Open"
    ).count()

    total_bookings = Booking.query.filter_by(
        user_id=user.id
    ).count()

    active_bookings = Booking.query.filter(
        Booking.user_id == user.id,
        Booking.status == "Booked"
    ).count()

    completed_treks = Booking.query.filter(
        Booking.user_id == user.id,
        Booking.status == "Completed"
    ).count()

    return jsonify({
        "available_treks": available_treks,
        "total_bookings": total_bookings,
        "active_bookings": active_bookings,
        "completed_treks": completed_treks
    }), 200


@trekker_bp.route("/treks", methods=["GET"])
@role_required("trekker")
def get_available_treks():
    search = request.args.get("search", "").strip()
    difficulty = request.args.get("difficulty", "").strip()
    location = request.args.get("location", "").strip()
    max_duration = request.args.get("max_duration", "").strip()

    query = Trek.query.filter_by(status="Open")

    if search:
        query = query.filter(
            db.or_(
                Trek.name.ilike(f"%{search}%"),
                Trek.location.ilike(f"%{search}%")
            )
        )

    if difficulty:
        query = query.filter_by(difficulty=difficulty)

    if location:
        query = query.filter(
            Trek.location.ilike(f"%{location}%")
        )

    if max_duration:
        try:
            duration = int(max_duration)

            if duration > 0:
                query = query.filter(
                    Trek.duration <= duration
                )
        except ValueError:
            return jsonify({
                "message": "Duration must be a valid number"
            }), 400

    treks = query.order_by(Trek.start_date.asc()).all()

    return jsonify({
        "treks": [trek.to_dict() for trek in treks]
    }), 200


@trekker_bp.route("/treks/<int:trek_id>", methods=["GET"])
@role_required("trekker")
def get_trek_details(trek_id):
    trek = db.session.get(Trek, trek_id)

    if trek is None or trek.status != "Open":
        return jsonify({
            "message": "Trek not found or not available"
        }), 404

    return jsonify({
        "trek": trek.to_dict()
    }), 200


@trekker_bp.route("/treks/<int:trek_id>/book", methods=["POST"])
@role_required("trekker")
def book_trek(trek_id):
    user = get_current_trekker()
    trek = db.session.get(Trek, trek_id)

    if trek is None:
        return jsonify({
            "message": "Trek not found"
        }), 404

    if trek.status != "Open":
        return jsonify({
            "message": "This trek is not open for booking"
        }), 400

    if trek.available_slots <= 0:
        return jsonify({
            "message": "No slots are available for this trek"
        }), 400

    existing_booking = Booking.query.filter(
        Booking.user_id == user.id,
        Booking.trek_id == trek.id,
        Booking.status.in_(["Booked", "Completed"])
    ).first()

    if existing_booking:
        return jsonify({
            "message": "You have already booked this trek"
        }), 409

    booking = Booking(
        user_id=user.id,
        trek_id=trek.id,
        booking_date=datetime.utcnow(),
        status="Booked",
        payment_status="Pending"
    )

    trek.available_slots -= 1

    db.session.add(booking)
    db.session.commit()

    return jsonify({
        "message": "Trek booked successfully",
        "booking": booking.to_dict()
    }), 201


@trekker_bp.route("/bookings", methods=["GET"])
@role_required("trekker")
def get_my_bookings():
    user = get_current_trekker()

    bookings = Booking.query.filter_by(
        user_id=user.id
    ).order_by(
        Booking.booking_date.desc()
    ).all()

    return jsonify({
        "bookings": [
            booking.to_dict()
            for booking in bookings
        ]
    }), 200


@trekker_bp.route(
    "/bookings/<int:booking_id>/cancel",
    methods=["PUT"]
)
@role_required("trekker")
def cancel_booking(booking_id):
    user = get_current_trekker()

    booking = db.session.get(Booking, booking_id)

    if booking is None or booking.user_id != user.id:
        return jsonify({
            "message": "Booking not found"
        }), 404

    if booking.status != "Booked":
        return jsonify({
            "message": "Only active bookings can be cancelled"
        }), 400

    if booking.trek.status in ["Ongoing", "Completed"]:
        return jsonify({
            "message": "This trek can no longer be cancelled"
        }), 400

    booking.status = "Cancelled"

    if booking.trek.available_slots < booking.trek.total_slots:
        booking.trek.available_slots += 1

    db.session.commit()

    return jsonify({
        "message": "Booking cancelled successfully",
        "booking": booking.to_dict()
    }), 200


@trekker_bp.route("/history", methods=["GET"])
@role_required("trekker")
def get_trekking_history():
    user = get_current_trekker()

    bookings = Booking.query.filter(
        Booking.user_id == user.id,
        Booking.status.in_(["Cancelled", "Completed"])
    ).order_by(
        Booking.booking_date.desc()
    ).all()

    return jsonify({
        "history": [
            booking.to_dict()
            for booking in bookings
        ]
    }), 200


@trekker_bp.route("/profile", methods=["GET"])
@role_required("trekker")
def get_profile():
    user = get_current_trekker()

    return jsonify({
        "user": user.to_dict()
    }), 200


@trekker_bp.route("/profile", methods=["PUT"])
@role_required("trekker")
def update_profile():
    user = get_current_trekker()
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

        user.name = name

    if "phone" in data:
        user.phone = str(data["phone"]).strip()

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully",
        "user": user.to_dict()
    }), 200