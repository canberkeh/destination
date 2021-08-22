from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from project.model import Base

engine = create_engine('sqlite:///project/database.db', connect_args={"check_same_thread": False})


db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
session = db_session()

Base.query = db_session.query_property()