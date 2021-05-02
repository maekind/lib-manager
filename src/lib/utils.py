#!/usr/bin/env python3
'''
Utils functions
'''
import hashlib
import uuid
from os import path
from pathlib import Path
from urllib.parse import unquote

__author__ = 'Marco Espinosa'
__version__ = '1.0'
__email__ = 'hi@marcoespinosa.com'


class Utils:
    '''
    Class to handle util functions
    '''

    @staticmethod
    def replace_special_chars(text):
        '''
        Replace special chars
        '''
        for ch in ['\\','`','*','_','{','}','[',']','(',')','>','#','+','-','.','!','$','\'', ':', '(', ')', '/']:
            if ch in text:
                text = text.replace(ch,"")

        return text

    @staticmethod
    def get_default_image():
        '''
        Function to fetch the default image file for unknowms
        '''
        with open(Path(".").resolve() / path.join("lib", "media", "res", "unknown.jpeg"), "br") as image_file:
            image = image_file.read()

        return image

    @staticmethod
    def unquote_file(file):
        '''
        Function to uquote a file string from a url
        @file: file url string to unquote
        @return: file unquoted
        '''
        return f"/{unquote(file)}"

    @staticmethod
    def hash_password(password, salt, bytes=512):
        '''
        Function that hash a password with a given salt
        @password: user plain-text password
        @salt: user configured salt
        @bytes: hash bytes. 512 by default. Options: 1, 256 or 512
        @return: passwor hashed in bytes
        '''
        if bytes == 1:
            # sha1
            return hashlib.sha1(password + salt).digest()
        elif bytes == 256:
            # sha256
            return hashlib.sha256(password + salt).digest()
        elif bytes == 512:
            # sha512 - default
            
            return hashlib.sha512(password + salt).digest()

        return None

    @staticmethod
    def get_salt():
        '''
        Function to return a new salt in bytes format
        @return: salt in bytes format
        '''
        return uuid.uuid4().bytes

