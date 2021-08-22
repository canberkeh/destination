'''Api entrypoint'''
from flasgger.utils import swag_from
from flask import jsonify, request
from run import app
from project.model import Country, City
from project.config.database import session
from project.config.swagger_setup import swagger, swagger_config


@app.route('/api/countries', methods=['GET'])
@swag_from('swagger/get_countries_config.yaml')
def get_country_list():
    '''Returns all countries in swagger'''
    countries = [country.serializer() for country in Country.query.all()]
    if countries:
        return jsonify(countries)
    return 'Country not found', 404


@app.route('/api/countries/<country_id>', methods=['GET'])
@swag_from('swagger/get_country_config.yaml')
def get_country(country_id):
    '''Returns country by id in swagger'''
    if not country_id.isnumeric() or int(country_id) <= 0:
        return 'Bad request', 400
    country = Country.query.filter_by(id=country_id).first()
    if country:
        country = country.serializer()
        return jsonify(country)
    return 'Country not found', 404


@app.route('/api/countries/<country_id>/cities', methods=['GET'])
@swag_from('swagger/get_cities_config.yaml')
def get_city_list(country_id):
    '''Returns cities by country_id in swagger'''
    if not country_id.isnumeric() or int(country_id) <= 0:
        return 'Bad request', 400
    city_list = City.query.filter_by(country_id=country_id).all()
    if city_list:
        cities = [city.serializer() for city in city_list]
        return jsonify(cities)
    return 'City not found', 404


@app.route('/api/countries/<country_id>/cities', methods=['POST'])
@swag_from('swagger/post_city_config.yaml')
def post_city(country_id):
    '''Create city by id in swagger'''
    if not country_id.isnumeric() or int(country_id) <= 0:
        return 'Bad request', 400
    try:
        input_json = request.get_json()
    except:
        return 'Bad request', 400
    city_name = input_json["name"]
    if not isinstance(city_name, int) and city_name:
        city_record = City(country_id=country_id, city_name=city_name)
        session.add(city_record)
        session.commit()
        return jsonify({
            'success': country_id + ' ' + city_name + ' posted!'
        })
    return 'Bad request', 400


@app.route('/api/countries/<city_id>/cities', methods=['DELETE'])
@swag_from('swagger/delete_city_config.yaml')
def delete_city(city_id):
    '''Delete city by id in swagger'''
    if not city_id.isnumeric() or int(city_id) <= 0:
        return 'Bad request', 400
    city = session.query(City).get(city_id)
    if city:
        session.delete(city)
        session.commit()
        return jsonify({
            'success': city.city_name + ' deleted'
        })
    return 'City not found', 404
