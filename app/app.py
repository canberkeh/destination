from flask import Flask, render_template, request, jsonify
from .model import *
from .database import Session
from .celery_worker import celery_app
import requests
from flask_mail import Mail, Message
from decouple import config
import sqlite3
from flasgger import Swagger
from flasgger.utils import swag_from


app = Flask(__name__)


# Flask-mail conf
app.config['MAIL_SERVER'] = 'smtp.live.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')
mail = Mail(app)


app.config['SWAGGER'] = {'TITLE': 'swagger', 'uiversion': 2}
swagger_config = {
    'headers': [],
    'specs': [
        {
            'endpoint': 'apispec_1',
            'route': '/apispec_1.json'
        }
    ],
    'static_url_path': "/flasgger_static",
    'swagger_ui': True,
    'specs_route': "/swagger/",
}

swagger = Swagger(app, config=swagger_config)


# Country list has been added to db via restcountries
country_list = Session.session.query(Country).all()
api_url = "https://restcountries.eu/rest/v2/name/"


# class AllCountryData(Resource):
#     def get(self):
#         # country = cur.execute('SELECT * FROM country;').fetchall()
#         country = Country.query.all()
#         result = users_schema.dump(country)
#         return jsonify(country)
# api.add_resource(AllCountryData, "/countryapi/all")


@app.route('/api/countries', methods=['GET'])
@swag_from('swagger/get_countries_config.yaml')
def get_country_list():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    countries = cur.execute(f'SELECT * FROM country;').fetchall()
    return jsonify(countries)


@app.route('/api/countries/<id>', methods=['GET'])
@swag_from('swagger/get_country_config.yaml')
def get_country(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    country = cur.execute(f'SELECT * FROM country where id={id};').fetchall()
    return jsonify(country)


@app.route('/api/countries/<country_id>/cities', methods=['GET'])
@swag_from('swagger/get_cities_config.yaml')
def get_city_list(country_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cities = cur.execute(f'SELECT * FROM city where country_id={country_id};').fetchall()
    return jsonify(cities)


@app.route('/api/countries/<country_id>/cities', methods=['POST'])
@swag_from('swagger/post_city_config.yaml')
def post_city(country_id):
    input_json = request.get_json()
    name = input_json["name"]

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    city = cur.execute(f'INSERT INTO city ("country_id", "city_name") VALUES ({country_id}, "{name}");')
    conn.commit()
    return jsonify({
        'success': 'success'
    })


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
            country = Session.session.query(Country).get(country_id)
            city_list = Session.session.query(City).filter_by(country_id=country_id).all()
            return render_template("country.html", country_list=country_list, selected_country=country, city_list=city_list)
        return render_template("country.html", country_list=country_list)


@app.route("/add_city", methods=["GET", "POST"])
def add_city():
    if request.method == "POST":
        country_id = request.form.get("country-id")
        city_name = request.form.get("city-name")
        city_record = City(country_id=country_id, city_name=city_name)
        Session.session.add(city_record)
        Session.session.commit()

        return render_template("country.html", country_list=country_list)
    else:
        return render_template("add_city.html", country_list=country_list)


@app.route("/destinations", methods=["GET", "POST"])
def destinations():
    if request.method == "POST":
        city_id = request.form.get("city-selector")
        if city_id != None:
            destination_list = Session.session.query(Description).filter_by(city_id=city_id).all()
            return render_template("country.html",country_list = country_list, city_id=city_id, destination_list=destination_list)
        else:
            return render_template("country.html", country_list=country_list)

@app.route("/add_destination", methods=["GET", "POST"])
def add_destination():
    city_id = request.form.get("city-id")
    description = request.form.get("add-destination")
    destination_record = Description(city_id=city_id, description=description)
    Session.session.add(destination_record)
    Session.session.commit()
    destination_list = Session.session.query(Description).filter_by(city_id=city_id).all()   ###### buraya gelince tekrar list_destinations çağırılabilir mi??
    return render_template("country.html", country_list=country_list, city_id=city_id, destination_list = destination_list)


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


