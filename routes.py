from flask import abort, Blueprint, jsonify, redirect, request, url_for
from http import HTTPStatus
import pymysql

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

	# /api/v1/api_status
	@routes_blueprint.route('/api_status', methods=['GET'])
	def api_status():
		try:
			db_status = 'DB_CONNECTED' if db.db_connection_status else "DB_DISCONNECTED"
			response = build_response('APP_RESPONDING. DB STATUS: ' + db_status, HTTPStatus.OK)
			return response
		except pymysql.MySQLError as sqle:
			abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
		except Exception as e:
			abort(HTTPStatus.BAD_REQUEST, description=str(e))

	# /api/v1/get_user
	@routes_blueprint.route('/get_user', methods=['POST'])
	def get_user():
		user_id = request.json.get('user_id')
		if not user_id:
			abort(HTTPStatus.BAD_REQUEST, description='MISSING_USER_ID')

		user = None
		try:
			user = db.get_entry(user_id)
			response = build_response({'user': user}, HTTPStatus.OK)
			return response
		except pymysql.MySQLError as sqle:
			abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
		except Exception as e:
			abort(HTTPStatus.BAD_REQUEST, description=str(e))

	# /
	@routes_blueprint.route('/', methods=['GET'])
	def main():
		return redirect(url_for('routes.api_status'))

	# /api/v1/update_user
	@routes_blueprint.route('/update_user', methods=['POST'])
	def update_user():
		user_details = request.json.get('user_details')
		user_id = request.json.get('user_id')
		if not user_details:
			abort(HTTPStatus.BAD_REQUEST, description='MISSING_USER_DETAILS')

		try:
			if not user_id:
				# Create new user
				db_user_id = db.add_entry(user_details)
			else:
				# Update existing user
				db_user_id = db.update_entry(entry_dict=user_details, entry_id=user_id)
			response = build_response({'user_id': db_user_id}, HTTPStatus.OK)
			return response
		except pymysql.MySQLError as sqle:
			abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
		except Exception as e:
			abort(HTTPStatus.BAD_REQUEST, description=str(e))


		user_id = db.add_entry(request.form.get('user_details'))
		response = build_response('SUCCESS', HTTPStatus.OK)
		return response

	return(routes_blueprint)