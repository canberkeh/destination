# Destination

### Dependencies

* [Python](https://www.python.org/) - Programming Language
* [Flask](https://flask.palletsprojects.com/) - The framework used
* [SQLAlchemy](https://docs.sqlalchemy.org/) - ORM
* [Alembic](https://alembic.sqlalchemy.org/) - Database Migrations
* [Flasgger](https://github.com/flasgger/flasgger) - Swagger tool
* [Celery](https://docs.celeryproject.org/en/stable/) - for Task Queues
* [Pip](https://pypi.org/project/pip/) - Dependency Management


**Install sqlite3**

  
    https://www.sqlite.org/download.html



### Virtual environments
```
$ pip install python-virtualenv
$ python -m venv venv
$ . venv/bin/activate

Install all project dependencies using:
```

Install all project dependencies using:

```
$ pip install -r requirements.txt
```
  
### Alembic Migrations

> 1- init alembic

    alembic init alembic

>

> 2- set alembic.ini file 

    >  sqlalchemy.url = sqlite:///app/database.db

>

> 3- set env.py in alembic folder

>

    > from app.model import Base

>

    > target_metadata = [Base.metadata]

>

> 4- generate first migration 

    > alembic revision --autogenerate -m "initial commit"

>

> 5- generate tables in db with upgrade 

    > alembic upgrade head

>

> 6- Run insert_to_db_from_api.py to insert country data to db

    >   python app\insert_to_db_from_api.py


### Start Celery worker

> 8- Run celery worker

    >   celery -A app.celery_worker worker --pool=solo -l info  (--pool=solo for windows)

### Run Project

```
    >   python app\run.py
```

-----------------------------
![s3](https://user-images.githubusercontent.com/73230039/126903970-876f2a24-a693-4751-ac3f-a3a90d3304c4.png)

![a1](https://user-images.githubusercontent.com/73230039/128763772-e4fd85d6-1bcb-4209-9185-cfb7005262f8.jpg)

-------------------------------------
![s22](https://user-images.githubusercontent.com/73230039/126903957-1e10a53e-a3f2-42a7-8cba-eacc291e01a5.png)
```
api_url = "https://restcountries.eu/rest/v2/name/"
```
-----------------------------------
