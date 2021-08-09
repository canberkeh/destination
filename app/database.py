from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///database.db', connect_args={"check_same_thread": False})

class Session():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()