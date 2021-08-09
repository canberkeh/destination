from celery import Celery
from decouple import config

celery_app = Celery('app',
            broker=config('BROKER_URL'),
            backend="amqp://",
            include = ['app.app'])
celery_app.conf.update(result_expires=3600,)


if __name__ == '__main__':
    celery_app.run(debug=True)
