from datetime import datetime

from extensions import db


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("treks.id"),
        nullable=False
    )

    booking_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Booked",
        nullable=False
    )

    payment_status = db.Column(
        db.String(20),
        default="Pending",
        nullable=False
    )

    payment_reference = db.Column(db.String(100))

    completed_at = db.Column(db.DateTime)

    cancelled_at = db.Column(db.DateTime)

    user = db.relationship(
        "User",
        back_populates="bookings"
    )

    trek = db.relationship(
        "Trek",
        back_populates="bookings"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "trek_id",
            name="unique_user_trek_booking"
        ),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user.name,
            "trek_id": self.trek_id,
            "trek_name": self.trek.name,
            "booking_date": self.booking_date.isoformat(),
            "status": self.status,
            "payment_status": self.payment_status,
            "payment_reference": self.payment_reference,
            "completed_at": (
                self.completed_at.isoformat()
                if self.completed_at
                else None
            ),
            "cancelled_at": (
                self.cancelled_at.isoformat()
                if self.cancelled_at
                else None
            )
        }