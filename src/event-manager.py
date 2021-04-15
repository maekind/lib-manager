#!/usr/bin/env python3 
'''
Event manager daemon
'''
import argparse
from flask import Flask

app = Flask(__name__)

author = 'Marco Espinosa'
version = '1.0'
email = 'hi@marcoespinosa.com'

@app.route('/')
def hello_message():
    return 'Event-manager for handling system file changes'


@app.route('/created/<path:file>')
def create_file(file):
    message = f'Create {file}'
    return message 

@app.route('/deleted/<path:file>')
def delete_file(file):
    message = f'Delete {file}'
    return message 

def main():
    '''
    Function Main
    '''
    parser = argparse.ArgumentParser(description='Event manager')

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
