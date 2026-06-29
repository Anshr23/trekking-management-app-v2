from datetime import datetime

from extensions import db


class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)

    location = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text)

    difficulty = db.Column(db.String(20), nullable=False)

    duration = db.Column(db.Integer, nullable=False)

    total_slots = db.Column(db.Integer, nullable=False)

    available_slots = db.Column(db.Integer, nullable=False)

    assigned_staff_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    status = db.Column(
        db.String(20),
        default="Pending",
        nullable=False
    )

    start_date = db.Column(db.Date, nullable=False)

    end_date = db.Column(db.Date, nullable=False)

    price = db.Column(db.Float, default=0.0)

    altitude = db.Column(db.Integer)

    image_url = db.Column(db.String(500))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    assigned_staff = db.relationship(
        "User",
        back_populates="assigned_treks",
        foreign_keys=[assigned_staff_id]
    )

    bookings = db.relationship(
        "Booking",
        back_populates="trek",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "difficulty": self.difficulty,
            "duration": self.duration,
            "total_slots": self.total_slots,
            "available_slots": self.available_slots,
            "assigned_staff_id": self.assigned_staff_id,
            "assigned_staff_name": (
                self.assigned_staff.name
                if self.assigned_staff
                else None
            ),
            "status": self.status,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "price": self.price,
            "altitude": self.altitude,
            "image_url": self.image_url
        }