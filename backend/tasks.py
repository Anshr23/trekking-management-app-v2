import csv
import os
from datetime import date, timedelta

from celery.schedules import crontab

from celery_app import celery
from extensions import db
from models import User, Trek, Booking


@celery.task
def send_daily_trek_reminders():
    today = date.today()
    upcoming_limit = today + timedelta(days=3)

    bookings = Booking.query.filter_by(
        status="Booked"
    ).all()

    reminders = []

    for booking in bookings:
        trek = booking.trek

        if (
            trek.start_date
            and today <= trek.start_date <= upcoming_limit
        ):
            reminder = {
                "user": booking.user.name,
                "email": booking.user.email,
                "trek": trek.name,
                "start_date": trek.start_date.isoformat()
            }

            reminders.append(reminder)

            print(
                f"REMINDER: {booking.user.email} - "
                f"{trek.name} starts on {trek.start_date}"
            )

    return {
        "message": "Daily reminders processed",
        "reminders_sent": len(reminders),
        "reminders": reminders
    }


@celery.task
def generate_monthly_admin_report():
    today = date.today()

    if today.month == 1:
        previous_month = 12
        previous_year = today.year - 1
    else:
        previous_month = today.month - 1
        previous_year = today.year

    completed_treks = Trek.query.filter(
        Trek.status == "Completed",
        db.extract("month", Trek.end_date) == previous_month,
        db.extract("year", Trek.end_date) == previous_year
    ).all()

    completed_bookings = Booking.query.join(Trek).filter(
        Booking.status == "Completed",
        db.extract("month", Trek.end_date) == previous_month,
        db.extract("year", Trek.end_date) == previous_year
    ).all()

    popular_trek = None
    popular_count = 0

    for trek in completed_treks:
        participant_count = Booking.query.filter_by(
            trek_id=trek.id,
            status="Completed"
        ).count()

        if participant_count > popular_count:
            popular_count = participant_count
            popular_trek = trek.name

    report_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Monthly Trekking Activity Report</title>
    </head>
    <body>
        <h1>Monthly Trekking Activity Report</h1>

        <p>
            Report for:
            {previous_month}/{previous_year}
        </p>

        <h2>Summary</h2>

        <ul>
            <li>
                Treks conducted:
                {len(completed_treks)}
            </li>

            <li>
                Total participants:
                {len(completed_bookings)}
            </li>

            <li>
                Most popular trek:
                {popular_trek or "No completed treks"}
            </li>

            <li>
                Popular trek participants:
                {popular_count}
            </li>
        </ul>
    </body>
    </html>
    """

    report_folder = celery.flask_app.config["REPORT_FOLDER"]
    os.makedirs(report_folder, exist_ok=True)

    filename = (
        f"monthly_report_"
        f"{previous_year}_{previous_month:02d}.html"
    )

    filepath = os.path.join(report_folder, filename)

    with open(filepath, "w", encoding="utf-8") as report_file:
        report_file.write(report_html)

    print(f"Monthly Admin report generated: {filepath}")

    return {
        "message": "Monthly Admin report generated successfully",
        "filename": filename,
        "treks_conducted": len(completed_treks),
        "participants": len(completed_bookings),
        "popular_trek": popular_trek
    }


@celery.task
def export_user_booking_history(user_id):
    user = db.session.get(User, user_id)

    if user is None or user.role != "trekker":
        return {
            "error": "Trekker not found"
        }

    bookings = Booking.query.filter_by(
        user_id=user.id
    ).order_by(
        Booking.booking_date.desc()
    ).all()

    export_folder = celery.flask_app.config["EXPORT_FOLDER"]
    os.makedirs(export_folder, exist_ok=True)

    filename = f"trekking_history_user_{user.id}.csv"
    filepath = os.path.join(export_folder, filename)

    with open(
        filepath,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "User ID",
            "Trek Name",
            "Location",
            "Booking Status",
            "Booking Date",
            "Trek Start Date",
            "Trek End Date"
        ])

        for booking in bookings:
            writer.writerow([
                user.id,
                booking.trek.name,
                booking.trek.location,
                booking.status,
                booking.booking_date.isoformat(),
                booking.trek.start_date.isoformat(),
                booking.trek.end_date.isoformat()
            ])

    return {
        "message": "CSV export completed",
        "filename": filename,
        "user_id": user.id
    }


celery.conf.beat_schedule = {
    "daily-trek-reminders": {
        "task": "tasks.send_daily_trek_reminders",
        "schedule": crontab(
            hour=9,
            minute=0
        )
    },

    "monthly-admin-report": {
        "task": "tasks.generate_monthly_admin_report",
        "schedule": crontab(
            day_of_month=1,
            hour=8,
            minute=0
        )
    }
}