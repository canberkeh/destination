from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from sqlalchemy.sql.functions import count
from sqlalchemy.util.langhelpers import NoneType
from .model import *
from .database import Session
from .celery_worker import celery_app
import requests
from flask_mail import Mail, Message
from decouple import config


app = Flask(__name__)


# Flask-mail conf
app.config['MAIL_SERVER'] = 'smtp.live.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')
mail = Mail(app)


# Country list has been added to db via restcountries
country_list = Session.session.query(Country).all()
api_url = "https://restcountries.eu/rest/v2/name/"


@app.route("/add_city", methods=["GET", "POST"])
def add_city():
    if request.method == "POST":
        country_id = request.form.get("country-selector")
        city_name = request.form.get("city-name")
        print(country_id, city_name)
        city_record = City(country_id=country_id, city_name=city_name)
        Session.session.add(city_record)
        Session.session.commit()

        return render_template("country.html", country_list=country_list)
    else:
        return render_template("add_city.html", country_list=country_list)

@app.route("/add_destination", methods=["GET", "POST"])
def add_destination():
    
    city_id = request.form.get("city-selector")
    description = request.form.get("add-destination")
    destination_record = Description(city_id=city_id, description=description)

    Session.session.add(destination_record)
    Session.session.commit()

    return render_template("city_list.html", country_list=country_list)



@app.route("/list_destinations", methods=["GET", "POST"])
def list_destinations():
    if request.method == "POST":
        id = request.form.get("city-selector")
        destination_list = Session.session.query(
            Description).filter_by(city_id=id).all()

    return render_template("destination_list.html", country_list=country_list, destination_list=destination_list)


@app.route("/send_destinations", methods=["GET", "POST"])
def send_destinations():
    if request.method == "POST":
        desc_id = request.form.getlist('send_destinations')
        email = request.form.get('email')
        send_data = []
        for description_id in desc_id:  # for ile değil/query içerisinde toplu olarak dönecek
            result = Session.session.query(
                Country, City, Description,
            ).filter(
                Country.id == City.country_id,
            ).filter(
                City.id == Description.city_id,
            ).filter(Description.id == int(description_id)).all()
            for i in result:
                send_data.append(i)
        msg = ""
        for data in send_data:
            (country, city, desc) = data
            msg += str(country) + ' ' + str(city) + ' ' + str(desc) + '\n'
        email_data = {
            'subject': 'Your destinations',
            'to': email,
            'body': msg
        }
        print(email_data)
        send_async_email.delay(email_data)
        return render_template("destination_list.html", country_list=country_list)


@celery_app.task(serializer='json')
def send_async_email(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['subject'],
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[email_data['to']])
    msg.body = email_data['body']
    with app.app_context():
        mail.send(msg)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("country-selector")
        if name != None:
            response_country = requests.get(api_url + name)
            country_info = response_country.json()
            return render_template("index.html", country_info=country_info, country_list=country_list)
        else:
            return render_template("index.html", country_list=country_list)
    else:
        return render_template("index.html", country_list=country_list)


@app.route('/country', methods=["GET"])
def country():
    return render_template("country.html", country_list=country_list)


@app.route('/city', methods=["GET", "POST"])
def city():
    if request.method == "POST":
        country_id = request.form.get("country-selector")
        if country_id != None:
            city_list = Session.session.query(City).filter_by(country_id=country_id).all()
            country_name = Session.session.query(Country).filter_by(id = country_id)
            return render_template("city.html", country_list = country_list, country_name = country_name, city_list = city_list)
        return render_template("country.html", country_list=country_list)


# def test():   # SMTP ile mail atılacak tüm veriler bu join ile çekilecek.
#     result = Session.session.query(
#         Country, City, Description,
#         ).filter(
#             Country.id==City.country_id,
#         ).filter(
#             City.id==Description.city_id,
#         ).filter(Description.id == 1).all()
#     list1=[]
#     for i in result:
#         list1.append(i)
#     print(list1)
# test()
