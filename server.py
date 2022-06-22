import os
import pymysql

from config import DevelopmentConfig as config_vars
#from config import ProductionConfig as config_vars
from db import Database
from flask import abort, Flask, jsonify, redirect, request, url_for
from flask_cors import CORS
from http import HTTPStatus

host = os.environ.get('FLASK_SERVER_HOST', config_vars.HOST)
port = os.environ.get('FLASK_SERVER_PORT', config_vars.PORT)
api_version = str(config_vars.API_VERSION).lower()
route_prefix = f"/api/{api_version}"

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app, resources={f"{route_prefix}/*": {"origins": "*"}})
    app.config.from_object(config_vars)
    return app

def get_response_msg(data, status_code):
    message = {
        'status': status_code,
        'data': data if data else 'No records found'
    }
    response_msg = jsonify(message)
    response_msg.status_code = status_code
    return response_msg

app = create_app()
wsgi_app = app.wsgi_app
db = Database(config_vars)

'''

-------------------------- ROUTES --------------------------

'''

## /api/v1/api_status
@app.route(f"{route_prefix}/api_status", methods=['GET'])
def api_status():
    try:
        db_status = 'DB_CONNECTED' if db.db_connection_status else "DB_DISCONNECTED"
        response = get_response_msg('APP_RESPONDING. DB STATUS: ' + db_status, HTTPStatus.OK)       
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))

## /
@app.route('/', methods=['GET'])
def main():
    return redirect(url_for('api_status'))

'''

-------------------------- ERROR HANDLING --------------------------

'''

## HTTP_400
@app.errorhandler(HTTPStatus.BAD_REQUEST)
def bad_request(e):
    return get_response_msg(str(e), HTTPStatus.BAD_REQUEST)

## HTTP_404
@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(e):    
    return get_response_msg(data=str(e), status_code=HTTPStatus.NOT_FOUND)


## HTTP_500
@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    return get_response_msg(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

'''

-------------------------- LAUNCH APP --------------------------

'''

if __name__ == '__main__':
    app.run(host=host, port=port)