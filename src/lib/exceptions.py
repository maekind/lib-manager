#!/usr/bin/env python3
'''
User-defined exceptions
'''


class UserExists(Exception):
    '''
    Raised when user already exists in database
    '''


class UpdateLibManagerStatusError(Exception):
    '''
    Raised when library manager status could not be done
    '''
