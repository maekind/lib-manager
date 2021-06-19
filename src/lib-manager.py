#!/usr/bin/env python3
# encoding:utf-8
'''
lib manager daemon
'''
import argparse
import sys
import os
import time
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from lib.database.connector import Db
from lib.media.scanner import Scanner
from lib.utils import Utils
from lib.logger import Logger


__author__ = 'Marco Espinosa'
__version__ = '1.0'
__email__ = 'hi@marcoespinosa.com'

SCANNER = Scanner(os.environ['LIB_FOLDER'])
APP = Flask(__name__)
# Only for public services
cors = CORS(APP, resources={r"/api/*": {"origins": "*"}})

# Configure logger
LOGGER = Logger("lib-manager")


@APP.route('/')
def hello_message():
    '''
    Prints hello message from flask server
    '''
    return 'Lib-manager for handling system file changes'


### PUBLIC API services

@APP.route('/api/get_albums')
def get_albums():
    '''
    Function to fetch albums info to database.
    @returns: json string
    '''
    message = 'get albums event received!'
    LOGGER.info(message)
    try:
        database = Db()
        LOGGER.info('Getting albums data ...')
        json_string = json.dumps(
            database.get_albums_data(), indent=4, sort_keys=True)

        return json_string
    except Exception as ex:

        LOGGER.error(f"Erro fetching album data. {ex} ")
        return ''


@APP.route('/api/login', methods=['POST', 'GET'])
def login():
    '''
    Function to perform a login into the application
    '''
    response = jsonify(message='NOK')

    if request.method == 'POST':
        database = Db()

    if request.method == 'POST':
        database = Db()
        # Get login data
        request_data = request.get_json()
        username = request_data['username']
        password = request_data['password']

        if database.valid_login(username, password):
            response = jsonify(message='OK')
        else:
            LOGGER.error('Invalid username/password')

    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@APP.route('/api/scan')
def scan_library():
    '''
    Function to handle scan library event
    '''
    # TODO: new thread?
    message = 'Scan library event received!'
    LOGGER.info(message)
    try:
        database = Db()
        LOGGER.info('Scanning library ...')
        songs, count, scan_time = SCANNER.scan(database)

        LOGGER.info(f'Processed files: {count} in {scan_time} seconds')
        return 'ok'
    except Exception as ex:
        LOGGER.error(f"Exception:{ex}")
        return 'nok'


@APP.route('/api/getstatus', methods=["GET"])
def get_status():
    '''
    Function to handle get status event
    '''
    database = Db()
    res = database.get_library_status()

    if res is not None:
        LOGGER.info(f"Library status fetched ({res})")
    else:
        LOGGER.error("Library status not set!")

    response = jsonify(message=res)

    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@APP.route('/api/setstatus', methods=['POST', 'GET'])
def set_status():
    '''
    Function to handle set status event
    '''
    response = jsonify(message='NOK')

    if request.method == 'POST':
        database = Db()
        request_data = request.get_json()
        status = request_data['status']

        if database.set_library_status(status) > 0:
            LOGGER.info(f"Library status set to {status} successfully.")
            response = jsonify(message='OK')
        else:
            LOGGER.error("Library status not set!")

    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

### END PUBLIC API services

### PRIVATE services


@APP.route('/created/<path:file>')
def create_file(file):
    '''
    Function to handle create file event
    '''
    message = f'Create {file} event received!'
    LOGGER.info(message)

    try:
        # TODO: Check format type
        start_time = time.time()
        database = Db()
        file_unquote = Utils.unquote_file(file)
        songs, count, scan_time = SCANNER.scan_file(file_unquote, database)
        LOGGER.info(f'File processed in {scan_time} seconds')

        end_time = (time.time() - start_time) / 60.0
        LOGGER.info(
            f'Music library updated successfully in {end_time} minutes.')
    except FileNotFoundError:
        LOGGER.error(f'File {file_unquote} not found!')

    return message


@APP.route('/deleted/<path:file>')
def delete_file(file):
    '''
    Function to handle delete file event
    '''
    message = f'Delete {file} event receiived!'
    LOGGER.info(message)

    # TODO: Check format type
    database = Db()
    file_unquote = Utils.unquote_file(file)
    res = database.delete_file(file_unquote)

    if res > 0:
        LOGGER.info(f"File '{file_unquote}' deleted successfully!")
    else:
        LOGGER.error("File not found in database!")

    return message

### END PRIVATE SERVICES


def init_db(freshdb):
    '''
    Function to initialize database at first time
    '''

    # Initialize database
    database = Db()
    try:
        database.init_db(freshdb)

    except Exception as ex:
        LOGGER.error(ex)
        sys.exit(1)


def main():
    '''
    Function Main
    '''
    parser = argparse.ArgumentParser(description='Lib manager')

    parser.add_argument('-a', '--address',
                        help='Webservice host address or FQDN.',
                        dest='address', metavar='STRING')

    parser.add_argument('-o', '--port',
                        help='Webservice port.',
                        dest='port', metavar='INT')

    parser.add_argument('-f', '--fresh-db',
                        help='''Set to True to start with a fresh database. 
                        All content and tables will be erased.''',
                        dest='freshdb', metavar='BOOLEAN')

    args = parser.parse_args()

    freshdb = False
    if args.freshdb is not None:
        freshdb = args.freshdb

    # Check for arguments
    if args.address is not None and args.port is not None:
        init_db(freshdb)
        APP.run(host=args.address, port=args.port, debug=False)
    else:
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    main()
