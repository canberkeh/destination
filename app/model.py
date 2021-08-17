from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    country_name = Column(String(80), nullable=False)
    city_relation = relationship("City", 
        cascade="all, delete", 
        passive_deletes=True, 
        backref="country"
    )

    def __repr__(self):
        return self.country_name

    def json(self):
        return {'country_name': self.country_name}


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

    def __repr__(self):
        return self.city_name


class Description(Base):
    __tablename__ = 'description'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('city.id', ondelete="CASCADE"))
    description = Column(Text, nullable=False)

    def __repr__(self):
        return self.description
