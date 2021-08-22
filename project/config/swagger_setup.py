'''Swagger configuration'''
from flasgger import Swagger
from run import app


app.config['SWAGGER'] = {'TITLE': 'swagger', 'uiversion': 2}
swagger_config = {
    'headers': [],
    'specs': [
        {
            'endpoint': 'swagger',
            'route': '/swagger.json'
        }
    ],
    'static_url_path': "/flasgger_static",
    'swagger_ui': True,
    'specs_route': "/swagger/",
    "info": {
        "title": "API Doc",
        "description": "API for my data",
        "contact": {
        "email": "canberkehorozal@gmail.com",
        "url": "https://github.com/canberkeh/",
        }
    }
}

swagger = Swagger(app, config=swagger_config)
