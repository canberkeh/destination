'''Script to add countries to db'''
import requests
from project.model import Country
from project.config.database import session

API_URL = "https://restcountries.eu/rest/v2/all"


def insert_to_db():
    '''Run script to insert country data to database from api'''
    response_country = requests.get(API_URL)
    country_info = response_country.json()

    country_list = []

    for country_dict in country_info:
        for element in country_dict.keys():
            if "name" in element:
                country_list.append(country_dict["name"])

    for each_country in country_list:
        country = Country(country_name=each_country)
        session.add(country)
        session.commit()
    print("Insert successful")

insert_to_db()
