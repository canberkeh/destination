from model import Country
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests


engine = create_engine('sqlite:///database.db', connect_args={"check_same_thread": False})


Base = declarative_base()
metadata = Base.metadata


DBSession = sessionmaker(bind=engine)
session = DBSession()


api_url = "https://restcountries.eu/rest/v2/all"


def insert_to_db():
    response_country = requests.get(api_url)
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