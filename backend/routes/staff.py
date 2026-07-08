from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity

from decorators import role_required
from extensions import db, cache
from models import User, Trek, Booking


staff_bp = Blueprint(
    "staff",
    __name__,
    url_prefix="/api/staff"
)


def get_current_staff():
    user_id = int(get_jwt_identity())
    return db.session.get(User, user_id)


def get_assigned_trek(trek_id, staff_id):
    return Trek.query.filter_by(
        id=trek_id,
        assigned_staff_id=staff_id
    ).first()


@staff_bp.route("/dashboard", methods=["GET"])
@role_required("staff")
def get_dashboard():
    staff = get_current_staff()

    assigned_treks = Trek.query.filter_by(
        assigned_staff_id=staff.id
    ).all()

    total_participants = 0

    for trek in assigned_treks:
        participant_count = Booking.query.filter(
            Booking.trek_id == trek.id,
            Booking.status.in_(["Booked", "Completed"])
        ).count()

        total_participants += participant_count

    ongoing_treks = sum(
        1
        for trek in assigned_treks
        if trek.status == "Ongoing"
    )

    completed_treks = sum(
        1
        for trek in assigned_treks
        if trek.status == "Completed"
    )

    return jsonify({
        "assigned_treks": len(assigned_treks),
        "total_participants": total_participants,
        "ongoing_treks": ongoing_treks,
        "completed_treks": completed_treks
    }), 200


@staff_bp.route("/treks", methods=["GET"])
@role_required("staff")
def get_my_treks():
    staff = get_current_staff()

    treks = Trek.query.filter_by(
        assigned_staff_id=staff.id
    ).order_by(
        Trek.start_date.asc()
    ).all()

    result = []

    for trek in treks:
        trek_data = trek.to_dict()

        trek_data["participant_count"] = Booking.query.filter(
            Booking.trek_id == trek.id,
            Booking.status.in_(["Booked", "Completed"])
        ).count()

        result.append(trek_data)

    return jsonify({
        "treks": result
    }), 200


@staff_bp.route(
    "/treks/<int:trek_id>/participants",
    methods=["GET"]
)
@role_required("staff")
def get_trek_participants(trek_id):
    staff = get_current_staff()

    trek = get_assigned_trek(trek_id, staff.id)

    if trek is None:
        return jsonify({
            "message": (
                "Trek not found or you are not assigned "
                "to manage this trek"
            )
        }), 404

    bookings = Booking.query.filter(
        Booking.trek_id == trek.id,
        Booking.status.in_(["Booked", "Completed"])
    ).order_by(
        Booking.booking_date.asc()
    ).all()

    participants = []

    for booking in bookings:
        participants.append({
            "booking_id": booking.id,
            "user_id": booking.user.id,
            "name": booking.user.name,
            "email": booking.user.email,
            "phone": booking.user.phone,
            "booking_date": booking.booking_date.isoformat(),
            "booking_status": booking.status,
            "payment_status": booking.payment_status
        })

    return jsonify({
        "trek": trek.to_dict(),
        "participants": participants
    }), 200


@staff_bp.route(
    "/treks/<int:trek_id>/slots",
    methods=["PUT"]
)
@role_required("staff")
def update_trek_slots(trek_id):
    staff = get_current_staff()

    trek = get_assigned_trek(trek_id, staff.id)

    if trek is None:
        return jsonify({
            "message": (
                "Trek not found or you are not assigned "
                "to manage this trek"
            )
        }), 404

    data = request.get_json()

    if not data or data.get("total_slots") is None:
        return jsonify({
            "message": "Total slots are required"
        }), 400

    try:
        new_total_slots = int(data["total_slots"])
    except (ValueError, TypeError):
        return jsonify({
            "message": "Total slots must be a valid number"
        }), 400

    if new_total_slots <= 0:
        return jsonify({
            "message": "Total slots must be greater than zero"
        }), 400

    booked_slots = trek.total_slots - trek.available_slots

    if new_total_slots < booked_slots:
        return jsonify({
            "message": (
                "Total slots cannot be less than "
                "already booked slots"
            )
        }), 400

    trek.total_slots = new_total_slots
    trek.available_slots = new_total_slots - booked_slots

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": "Trek slots updated successfully",
        "trek": trek.to_dict()
    }), 200


@staff_bp.route(
    "/treks/<int:trek_id>/status",
    methods=["PUT"]
)
@role_required("staff")
def update_trek_status(trek_id):
    staff = get_current_staff()

    trek = get_assigned_trek(trek_id, staff.id)

    if trek is None:
        return jsonify({
            "message": (
                "Trek not found or you are not assigned "
                "to manage this trek"
            )
        }), 404

    data = request.get_json()

    if not data or not data.get("status"):
        return jsonify({
            "message": "Trek status is required"
        }), 400

    new_status = str(data["status"]).strip().title()

    allowed_statuses = [
        "Open",
        "Closed",
        "Ongoing",
        "Completed"
    ]

    if new_status not in allowed_statuses:
        return jsonify({
            "message": "Invalid trek status"
        }), 400

    if trek.status == "Completed":
        return jsonify({
            "message": "A completed trek cannot be reopened"
        }), 400

    trek.status = new_status

    if new_status == "Completed":
        active_bookings = Booking.query.filter_by(
            trek_id=trek.id,
            status="Booked"
        ).all()

        for booking in active_bookings:
            booking.status = "Completed"

    db.session.commit()
    cache.clear()

    return jsonify({
        "message": f"Trek status updated to {new_status}",
        "trek": trek.to_dict()
    }), 200