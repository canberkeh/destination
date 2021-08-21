from decouple import config
from app import app
from flask_mail import Mail, Message
# Flask-mail conf

mail = Mail(app)

class SmtpConfig():
    app.config['MAIL_SERVER'] = 'smtp.live.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = config('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')