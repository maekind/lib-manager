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
from flask import Flask
from flask import request
from lib.database.connector import Db
from lib.media.scanner import Scanner
from lib.utils import Utils
from lib.logger import Logger


__author__ = 'Marco Espinosa'
__version__ = '1.0'
__email__ = 'hi@marcoespinosa.com'

scanner = Scanner(os.environ['LIB_FOLDER'])
app = Flask(__name__)

# Configure logger
logger = Logger("lib-manager")


@app.route('/')
def hello_message():
    '''
    Prints hello message from flask server
    '''
    return 'Lib-manager for handling system file changes'


@app.route('/get_albums')
def get_albums():
    '''
    Function to fetch albums info to database.
    @returns: json string 
    '''
    message = f'get albums event received!'
    logger.info(message)
    try:
        database = Db()
        logger.info(f'Getting albums data ...')
        json_string = json.dumps(database.get_albums_data(), indent=4, sort_keys=True)
        
        return json_string
    except Exception as ex:
     
        logger.error(f"Erro fetching album data. {ex} ")
        return ''

@app.route('/login', methods=['POST', 'GET'])
def login():
    '''
    Function to perform a login into the application
    '''
    if request.method == 'POST':
        database = Db()
        if database.valid_login(request.form['username'],
                                request.form['password']):
            return 'ok'
        else:
            logger.error('Invalid username/password')

    return 'nok'


@app.route('/scan')
def scan_library():
    '''
    Function to handle scan library event
    '''
    # TODO: new thread?
    message = f'Scan library event received!'
    logger.info(message)
    try:
        database = Db()
        logger.info(f'Scanning library ...')
        songs, count, scan_time = scanner.scan(database)

        logger.info(f'Processed files: {count} in {scan_time} seconds')
        return 'ok'
    except:
        return 'nok'


@app.route('/created/<path:file>')
def create_file(file):
    '''
    Function to handle create file event
    '''
    message = f'Create {file} event received!'
    logger.info(message)

    try:
        # TODO: Check format type
        start_time = time.time()
        database = Db()
        file_unquote = Utils.unquote_file(file)
        songs, count, scan_time = scanner.scan_file(file_unquote, database)
        logger.info(f'File processed in {scan_time} seconds')

        end_time = (time.time() - start_time) / 60.0
        logger.info(
            f'Music library updated successfully in {end_time} minutes.')
    except FileNotFoundError:
        logger.error(f'File {file_unquote} not found!')

    return message


@app.route('/deleted/<path:file>')
def delete_file(file):
    '''
    Function to handle delete file event
    '''
    message = f'Delete {file} event receiived!'
    logger.info(message)

    # TODO: Check format type
    database = Db()
    file_unquote = Utils.unquote_file(file)
    res = database.delete_file(file_unquote)

    if res > 0:
        logger.info(f"File '{file_unquote}' deleted successfully!")
    else:
        logger.error("File not found in database!")

    return message


def init_db(freshdb):
    '''
    Function to initialize database at first time
    '''
    # Initialize database
    database = Db()
    try:
        database.init_db(freshdb)

    except Exception as e:
        logger.error(e)
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
                        help='Set to True to start with a fresh database. All content and tables will be erased.',
                        dest='freshdb', metavar='BOOLEAN')

    args = parser.parse_args()

    freshdb = False
    if args.freshdb is not None:
        freshdb = args.freshdb

    # Check for arguments
    if args.address is not None and args.port is not None:
       #init_db(freshdb)
        app.run(host=args.address, port=args.port, debug=False)
    else:
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    main()
