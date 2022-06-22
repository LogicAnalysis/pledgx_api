from flask import Blueprint, jsonify, redirect, url_for
from http import HTTPStatus

from db import Database

def build_response(data, status_code):
    message = {
        'data': data if data else 'NO_DATA',
        'status': status_code
    }
    response_msg = jsonify(message)
    response_msg.status_code = status_code
    return response_msg

def construct_routes_blueprint(db):

    routes_blueprint = Blueprint('routes', __name__)

    # /test_route
    @routes_blueprint.route('/test_route', methods=['GET'])
    def test():
        db_status = 'DB_CONNECTED' if db.db_connection_status else "DB_DISCONNECTED"
        return build_response('APP_RESPONDING. DB STATUS: ' + db_status, HTTPStatus.OK)

    return(routes_blueprint)

    ## /
    @routes_blueprint.route('/', methods=['GET'])
    def main():
        return redirect(url_for('api_status'))