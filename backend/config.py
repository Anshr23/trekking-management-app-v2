import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

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

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/1"
    CACHE_DEFAULT_TIMEOUT = 300

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_USERNAME")

    ADMIN_REPORT_EMAIL = os.environ.get(
        "ADMIN_REPORT_EMAIL",
        "admin@tma.com"
    )