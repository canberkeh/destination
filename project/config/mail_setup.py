'''Mail configuration'''
from decouple import config
from flask_mail import Mail
from run import app


def mail_config():
    '''flask-mail configuration'''
    app.config['MAIL_SERVER'] = 'smtp.live.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = config('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')
    mail = Mail(app)
    return mail
