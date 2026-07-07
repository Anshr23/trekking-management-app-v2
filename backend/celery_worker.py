from app import app
from celery_app import celery

import tasks


celery.flask_app = app