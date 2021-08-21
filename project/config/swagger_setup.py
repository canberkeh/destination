from flasgger import Swagger

def swagger_config(app):
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
    }

    swagger = Swagger(app, config=swagger_config)
