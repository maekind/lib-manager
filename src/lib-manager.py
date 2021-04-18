#!/usr/bin/env python3
'''
lib manager daemon
'''
import argparse
import logging
import sys
import os
from flask import Flask
from lib.database.connector import Db
from sqlalchemy.exc import OperationalError
from lib.media.scanner import Scanner

author = 'Marco Espinosa'
version = '1.0'
email = 'hi@marcoespinosa.com'

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
    return 'Event-manager for handling system file changes'


@app.route('/created/<path:file>')
def create_file(file):
    message = f'Create {file}'
    logger.info(message)
    return message


@app.route('/deleted/<path:file>')
def delete_file(file):
    message = f'Delete {file}'
    logger.info(message)
    return message

def init_db():
    '''
    Function to initialize database at first time
    '''
    # Initialize database
    database = Db(logger)
    try:
        result = database.init_db()
        # If tables created, we perform a forlder scan
        # to initialize database
        result = True
        if result:
            scanner = Scanner(os.environ['LIB_FOLDER'])
            songs, count, time = scanner.scan()
            logger.info(f'Processed files: {count} in {time} seconds')
    except OperationalError as e:
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

    args = parser.parse_args()

    # Check for arguments
    if args.address is not None and args.port is not None:
        init_db()
        app.run(host=args.address, port=args.port)
    else:
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    main()
