import os
import pymysql

#from flask import abort, Flask, jsonify, redirect, request, url_for
from flask import abort, Flask, jsonify
from flask_cors import CORS
from http import HTTPStatus

from config import DevelopmentConfig as config_vars
#from config import ProductionConfig as config_vars
from db import Database
from error_handler import error_handler_blueprint
from routes import construct_routes_blueprint

host = os.environ.get('FLASK_SERVER_HOST', config_vars.HOST)
port = os.environ.get('FLASK_SERVER_PORT', config_vars.PORT)
api_version = str(config_vars.API_VERSION).lower()
route_prefix = f'/api/{api_version}'

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(construct_routes_blueprint(Database(config_vars)), url_prefix=f'/{route_prefix}')
    app.register_blueprint(error_handler_blueprint)
    cors = CORS(app, resources={f'{route_prefix}/*': {'origins': '*'}})
    app.config.from_object(config_vars)
    return app

app = create_app()
wsgi_app = app.wsgi_app

if __name__ == '__main__':
    app.run(host=host, port=port)