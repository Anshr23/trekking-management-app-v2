from flask import Flask, jsonify
from flask_cors import CORS
from routes.admin import admin_bp
from routes.trekker import trekker_bp

from config import Config
from extensions import db, jwt

from models import User

from routes.auth import auth_bp
from routes.staff import staff_bp

import os

from celery_app import init_celery

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    os.makedirs(
        app.config["EXPORT_FOLDER"],
        exist_ok=True
    )

    os.makedirs(
        app.config["REPORT_FOLDER"],
        exist_ok=True
    )

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    init_celery(app)
    #celery.flask_app = app

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(trekker_bp)
    app.register_blueprint(staff_bp)

    with app.app_context():
        db.create_all()
        create_default_admin()

    @app.route("/")
    def home():
        return jsonify({
            "message": "Trekking Management Application V2 API is running"
        })

    return app


def create_default_admin():
    admin = User.query.filter_by(role="admin").first()

    if admin is None:
        admin = User(
            name="Admin",
            email="admin@tma.com",
            role="admin"
        )

        admin.set_password("admin123")

        db.session.add(admin)
        db.session.commit()

        print("Default admin created.")
        print("Email: admin@tma.com")
        print("Password: admin123")


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5001, use_reloader=False)