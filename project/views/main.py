'''Main entrypoint'''
from flask import render_template, request
import requests
from flask_mail import Message
from run import app
from project.model import Country, City, Destination
from project.config.database import session
from project.config.celery_worker import celery_app
from project.config.mail_setup import mail_config


# Country list has been added to db via restcountries
API_URL = "https://restcountries.eu/rest/v2/name/"
country_list = session.query(Country).all()


@app.route('/', methods=["GET", "POST"])
def index():
    '''Homepage'''
    if request.method == "POST":
        name = request.form.get("country-selector")
        if name:
            response_country = requests.get(API_URL + name)
            country_info = response_country.json()
            return render_template("index.html", country_info=country_info,
                                                 country_list=country_list)
        return render_template("index.html", country_list=country_list)
    return render_template("index.html", country_list=country_list)


@app.route('/country', methods=["GET"])
def list_country():
    '''Returns all countries'''
    return render_template("country.html", country_list=country_list)


@app.route('/city', methods=["GET", "POST"])
def list_city():
    '''Returns city list by country_id'''
    if request.method == "POST":
        country_id = request.form.get("country-selector")
        if country_id:
            country = session.query(Country).get(country_id)
            city_list = session.query(City).filter_by(
                country_id=country_id).all()
            return render_template("country.html", country_list=country_list,
                                                   selected_country=country, city_list=city_list)
    return render_template("country.html", country_list=country_list)


@app.route("/add_city", methods=["GET", "POST"])
def add_city():
    '''Create city by country_id'''
    if request.method == "POST":
        country_id = request.form.get("country-id")
        city_name = request.form.get("city-name")
        city_record = City(country_id=country_id, city_name=city_name)
        session.add(city_record)
        session.commit()
        return render_template("country.html", country_list=country_list)
    return render_template("add_city.html", country_list=country_list)


@app.route("/destinations", methods=["GET", "POST"])
def list_destinations():
    '''Returns destinations by city_id'''
    if request.method == "POST":
        city_id = request.form.get("city-selector")
        if city_id:
            destination_list = session.query(
                Description).filter_by(city_id=city_id).all()
            return render_template("country.html", country_list=country_list,
                                                   city_id=city_id,
                                                   destination_list=destination_list)
        return render_template("country.html", country_list=country_list)
    return render_template("country.html", country_list=country_list)


@app.route("/add_destination", methods=["GET", "POST"])
def add_destination():
    '''Create destination by city_id'''
    city_id = request.form.get("city-id")
    description = request.form.get("add-destination")
    destination_record = Description(city_id=city_id, description=description)
    session.add(destination_record)
    session.commit()
    destination_list = session.query(
        Description).filter_by(city_id=city_id).all()
    return render_template("country.html", country_list=country_list,
                                           city_id=city_id,
                                           destination_list=destination_list)


@app.route("/send_destinations", methods=["GET", "POST"])
def send_destinations():
    '''Send choosen destinations to the celery worker'''
    if request.method == "POST":
        desc_id = request.form.getlist('send_destinations')
        email = request.form.get('email')
        send_data = []
        for description_id in desc_id:  # for ile değil/query içerisinde toplu olarak dönecek
            result = session.query(
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
            msg += f" * {str(country.country_name)} {str(city.city_name)} {str(desc)}\n"
        email_data = {
            'subject': 'Your destinations',
            'to': email,
            'body': msg
        }
        print(email_data)
        send_async_email.delay(email_data)
    return render_template("country.html", country_list=country_list)


@celery_app.task(serializer='json')
def send_async_email(email_data):
    '''Background task to send an email with Flask-Mail.'''
    mail = mail_config()
    msg = Message(email_data['subject'],
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    with app.app_context():
        mail.send(msg)
