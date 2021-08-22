'''Setup for celery worker, connection with cloudamqp'''
from celery import Celery
from decouple import config


celery_beat_schedule = {
    "schedule": 5.0,   # In seconds
}


celery_app = Celery('main',
                    broker=config('BROKER_URL'),
                    backend="amqp://",
                    include=['project.views.main'])

celery_app.conf.update(result_expires=3600,
                       beat_schedule=celery_beat_schedule,)


if __name__ == '__main__':
    celery_app.run(debug=True)
