# from app import app
# from flask import jsonify
# import werkzeug
# werkzeug.cached_property = werkzeug.utils.cached_property
# import flask.scaffold
# flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
# from flask_restplus import Api, Resource, reqparse
# from .database import Session
# from .model import *

# api = Api(app)
# parser = reqparse.RequestParser()


# @api.route('/countryapi/<string:id>')
# class CountryApi(Resource):
#     @api.doc(parser=parser)
#     def get(self, id):
#         country = Session.session.query(Country).get(id)
#         print(country)
#         args = parser.parse_args()
#         country_name = args['country']
#         print(country_name)
#         country_name = jsonify(country_name)
#         print(country_name)
#         return country_name



# # namespace = flask_api.namespace('main', description='Main APIs')


# # @namespace.route("/busra")
# # class MainClass(Resource):
# #   def get(self):
# #     return {
# #       "status": "Got new data"
# #     }
# #   def post(self):
# #     return {
# #       "status": "Posted new data"
# #     }





