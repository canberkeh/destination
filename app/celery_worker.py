from celery import Celery
from decouple import config


celery_beat_schedule = {
    "schedule": 5.0, # In seconds
}


celery_app = Celery('app',
            broker=config('BROKER_URL'),
            backend="amqp://",
            include = ['app.app'])

celery_app.conf.update(result_expires=3600, beat_schedule=celery_beat_schedule,)


if __name__ == '__main__':
    celery_app.run(debug=True)
