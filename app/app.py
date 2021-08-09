from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from sqlalchemy.util.langhelpers import NoneType
from model import *
from database import Session
import requests
from flask_mail import Mail, Message
from celery_worker import celery_app


app = Flask(__name__)


# Country list has been added to db via restcountries
country_list = Session.session.query(Country).all()
api_url = "https://restcountries.eu/rest/v2/name/"


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


@app.route('/destinations', methods=["GET", "POST"])
def destinations():
    return render_template("destinations.html", country_list=country_list)


@app.route("/add_city", methods=["GET", "POST"])
def add_city():
    country_id = request.form.get("country-selector")
    city_name = request.form.get("add-city")

    city_record = City(country_id=country_id, city_name=city_name)
    Session.session.add(city_record)
    Session.session.commit()

    return render_template("destinations.html", country_list=country_list)


@app.route('/list_cities', methods=["GET", "POST"])
def list_cities():
    if request.method == "POST":
        id = request.form.get("country-selector")
        city_list = Session.session.query(City).filter_by(country_id=id).all()
    return render_template("city_list.html", country_list=country_list, city_list=city_list)


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
        send_async_email()
    return render_template("destinations_test.html", send_data=send_data)


# Flask-mail conf
app.config['MAIL_SERVER'] = 'smtp.live.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'testpython1192@hotmail.com'
app.config['MAIL_PASSWORD'] = 'berke1192'
mail = Mail(app)


@celery_app.task
def send_async_email():
    """Background task to send an email with Flask-Mail."""
    try:
        msg = Message("Deneme test mail",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=["testmail@gmail.com"])
        msg.body = "Merhaba!\n Test Deneme Mail"
        mail.send(msg)
        return 'Mail başarıyla gönderildi!'
    except Exception as e:
        return(str(e))


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
