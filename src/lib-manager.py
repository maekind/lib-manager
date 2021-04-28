#!/usr/bin/env python3
'''
lib manager daemon
'''
import argparse
import logging
import sys
import os
import time
from flask import Flask
from lib.database.connector import Db
from lib.media.scanner import Scanner
from urllib.parse import unquote


author = 'Marco Espinosa'
version = '1.0'
email = 'hi@marcoespinosa.com'

scanner = Scanner(os.environ['LIB_FOLDER'])
app = Flask(__name__)


def configure_logging(name):
    '''
    Function to configure loggind
    @name: logger name
    @return logger
    '''
    level = logging.DEBUG

    log_setup = logging.getLogger(name)

    # Formatting logger output
    formatter = logging.Formatter(
        "%(asctime)s [%(name)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Setting logger to console
    log_handler = logging.StreamHandler()

    # Setting formatter
    log_handler.setFormatter(formatter)

    # Setting level
    log_setup.setLevel(level)

    # Creating handler to configured logger
    log_setup.addHandler(log_handler)

    # Set logger
    return logging.getLogger(name)


# Configure logger
logger = configure_logging("lib-manager")


@app.route('/')
def hello_message():
    return 'Lib-manager for handling system file changes'


@app.route('/created/<path:file>')
def create_file(file):
    message = f'Create {file}'
    logger.info(message)

    try:
        start_time = time.time()
        database = Db(logger)
        file_unquote = f"/{unquote(file)}"
        songs, count, scan_time = scanner.scan_file(file_unquote, database)
        logger.info(f'File processed in {scan_time} seconds')
        
        end_time = (time.time() - start_time) / 60.0
        logger.info(f'Music library updated successfully in {end_time} minutes.')
    except FileNotFoundError:
        logger.error(f'File {file_unquote} not found!')

    return message


@app.route('/deleted/<path:file>')
def delete_file(file):
    message = f'Delete {file}'
    logger.info(message)
    
    database = Db(logger)
    file_unquote = f"/{unquote(file)}"
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
    database = Db(logger)
    try:
        database.init_db(freshdb)
        logger.info(f'Scanning library ...')
        # scanner = Scanner(os.environ['LIB_FOLDER'])
        songs, count, scan_time = scanner.scan(database)
        logger.info(f'Processed files: {count} in {scan_time} seconds')

        #logger.info(f'Saving music data into the database...')
        start_time = time.time()
        # For each song
        # for song in songs:
        #     id = database.add_song(song)
        
        end_time = (time.time() - start_time) / 60.0
        
        logger.info(f'Music library updated successfully in {end_time} minutes.')

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
        freshdb =args.freshdb
    

    # Check for arguments
    if args.address is not None and args.port is not None:
        #init_db(freshdb)
        app.run(host=args.address, port=args.port)
    else:
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    main()
