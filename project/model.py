from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from project.config.database import Base

class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    country_name = Column(String(80), nullable=False)
    city_relation = relationship("City", 
        cascade="all, delete", 
        passive_deletes=True, 
        backref="country"
    )

    def serializer(self):
        return {
            'id': self.id,
            'name': self.country_name
        }


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('country.id', ondelete="CASCADE"))
    city_name = Column(String(80), nullable=False)
    description_relation = relationship("Description", 
        cascade="all, delete", 
        passive_deletes=True, 
        backref="city"
    )

    def serializer(self):
        return {
            "id": self.id,
            "country_id": self.country_id,
            "city_name": self.city_name
        }


class Description(Base):
    __tablename__ = 'description'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('city.id', ondelete="CASCADE"))
    description = Column(Text, nullable=False)

    def __repr__(self):
        return self.description
