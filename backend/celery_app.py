from celery import Celery


celery = Celery(
    "trekking_management",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


def init_celery(app):
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        timezone="Asia/Kolkata",
        enable_utc=False
    )

    class FlaskTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = FlaskTask
    celery.flask_app = app

    return celery