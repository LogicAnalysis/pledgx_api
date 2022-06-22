import os
import json

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MAIN_CONFIG = {}


def load_from_json(json_file, key):
    '''
    Retrieves vars from a json file
    '''
    global MAIN_CONFIG
    try:
        with open(os.path.join(BASE_DIR, json_file)) as config_file:
            MAIN_CONFIG = {**MAIN_CONFIG, **json.load(config_file)[key]}

    except Exception as e:
        raise Exception(f'Failed to load json file ({_json_filepath}). Error: {e}')


class Config(object):
    '''
    Initiates shared config variables for the app
    '''

    # Load config file
    load_from_json(json_file='settings.json', key='main')

    # Get API Version
    API_VERSION = MAIN_CONFIG['common']['API_VERSION']

    # Get DB Server config
    HOST = MAIN_CONFIG['common']['HOST']
    PORT = MAIN_CONFIG['common']['PORT']


class ProductionConfig(Config):
    '''
    Configuration specific to production environment
    '''

    # Load secrets file
    load_from_json(json_file='secrets.json', key='production_secrets')

    # CSRF
    CSRF_ENABLED = MAIN_CONFIG['env']['production']['CSRF_ENABLED']
    CSRF_SESSION_KEY = MAIN_CONFIG['env']['production']['CSRF_SESSION_KEY']

    # DB
    CONNECTION_TIMEOUT = MAIN_CONFIG['DATABASE_SETTINGS']['CONNECTION_TIMEOUT']
    DB_HOST = MAIN_CONFIG['DATABASE_SETTINGS']['DB_HOST']
    DB_NAME = MAIN_CONFIG['DATABASE_SETTINGS']['DB_NAME']
    DB_PORT = MAIN_CONFIG['DATABASE_SETTINGS']['DB_PORT']
    DB_PASSWORD = MAIN_CONFIG['DATABASE_SETTINGS']['DB_PASSWORD']
    DB_USER = MAIN_CONFIG['DATABASE_SETTINGS']['DB_USER']

    # Environment
    DEBUG = MAIN_CONFIG['env']['production']['DEBUG']
    DEVELOPMENT = MAIN_CONFIG['env']['production']['DEVELOPMENT']
    ENV = MAIN_CONFIG['env']['production']['ENV']


class DevelopmentConfig(Config):
    '''
    Configuration specific to development environment
    '''

    # Load secrets file
    load_from_json(json_file='secrets.json', key='development_secrets')

    # CSRF
    CSRF_ENABLED = MAIN_CONFIG['env']['development']['CSRF_ENABLED']

    # DB
    CONNECTION_TIMEOUT = MAIN_CONFIG['DATABASE_SETTINGS']['CONNECTION_TIMEOUT']
    DB_HOST = MAIN_CONFIG['DATABASE_SETTINGS']['DB_HOST']
    DB_NAME = MAIN_CONFIG['DATABASE_SETTINGS']['DB_NAME']
    DB_PORT = MAIN_CONFIG['DATABASE_SETTINGS']['DB_PORT']
    DB_PASSWORD = MAIN_CONFIG['DATABASE_SETTINGS']['DB_PASSWORD']
    DB_USER = MAIN_CONFIG['DATABASE_SETTINGS']['DB_USER']

    # Environment
    DEBUG = MAIN_CONFIG['env']['development']['DEBUG']
    DEVELOPMENT = MAIN_CONFIG['env']['development']['DEVELOPMENT']
    ENV = MAIN_CONFIG['env']['development']['ENV']