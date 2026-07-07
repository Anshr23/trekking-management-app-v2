import os
from datetime import timedelta

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(BASE_DIR, "trekking.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "trekking-management-secret-key"

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)

    #for celery
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

    REDIS_URL = "redis://localhost:6379/1"

    EXPORT_FOLDER = os.path.join(BASE_DIR, "exports")
    REPORT_FOLDER = os.path.join(BASE_DIR, "reports")