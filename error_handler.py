from flask import Blueprint, jsonify
from http import HTTPStatus

error_handler_blueprint = Blueprint('error_handler', __name__)

def build_error_response(error, status_code):
	'''
	Builds the error response
	'''
	response = jsonify({'data': str(error), 'status': status_code})
	response.status_code = status_code
	return response

# HTTP_400
@error_handler_blueprint.app_errorhandler(HTTPStatus.BAD_REQUEST)
def bad_request(e):
	return build_error_response(e, HTTPStatus.BAD_REQUEST)

# HTTP_404
@error_handler_blueprint.app_errorhandler(HTTPStatus.NOT_FOUND)
def not_found(e):
	return build_error_response(e, HTTPStatus.NOT_FOUND)

# HTTP_405
@error_handler_blueprint.app_errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
def method_not_allowed(e):
	return build_error_response(e, HTTPStatus.METHOD_NOT_ALLOWED)

# HTTP_500
@error_handler_blueprint.app_errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_server_error(e):
	return build_error_response(e, HTTPStatus.INTERNAL_SERVER_ERROR)