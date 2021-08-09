from celery import Celery
from app import app



celery_beat_schedule = {
    "time_scheduler": {
        "task": "app.send_mail",
        "schedule": 5.0, # In seconds
    }
}

celery = Celery(app.name)


celery.conf.update(
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    broker_url=app.config["CELERY_BROKER_URL"],
    timezone="UTC",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    beat_schedule=celery_beat_schedule,
)


def show(send_data, email):
    print(send_data, email)


# @celery.task
# def send_mail_to_mq():
#     email = app.send_celery.email
#     print(email)