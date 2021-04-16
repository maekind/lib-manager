#!/usr/bin/env python3
'''
lib manager daemon
'''
import argparse
import logging
from flask import Flask

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
logger = configure_logging("file-observer")


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
        app.run(host=args.address, port=args.port)
    else:
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    main()
