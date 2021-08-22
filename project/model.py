'''Database Models'''
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Country(Base):
    '''
    Country model
    id : int, pk
    name : str, not null
    '''
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    country_name = Column(String(80), nullable=False)
    city_relation = relationship("City",
                                 cascade="all, delete",
                                 passive_deletes=True,
                                 backref="country")

    def serializer(self):
        '''Returns json result to use in swagger ui'''
        return {
            'id': self.id,
            'name': self.country_name
        }


class City(Base):
    '''
    City model
    id : int, pk
    country_id : int, country relation --> country.id=city.country_id
    city_name : str, not null
    '''
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('country.id', ondelete="CASCADE"))
    city_name = Column(String(80), nullable=False)
    destination_relation = relationship("Destination",
                                        cascade="all, delete",
                                        passive_deletes=True,
                                        backref="city")

    def serializer(self):
        '''Returns json result to use in swagger ui'''
        return {
            "id": self.id,
            "country_id": self.country_id,
            "city_name": self.city_name
        }


class Destination(Base):
    '''
    Destination model
    id : int, pk
    city_id : int, relation --> city.id=destination.city_id
    destination : str, not null
    '''
    __tablename__ = 'destination'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('city.id', ondelete="CASCADE"))
    destination = Column(Text, nullable=False)
