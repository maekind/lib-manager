#!/usr/bin/env python3
'''
Utils functions
'''
import bcrypt
import re
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
    def format_string(str):
        '''
        Checks if string is null or empty or only have whitespaces
        '''
        new_str = "Unknown"

        # if str is not not we check for leading whitespaces and return srt  
        if str is not None and str != "":
            if re.match('^ +', str):
                str = str.lstrip()
            
            return str
        else:
            return new_str

    @staticmethod
    def replace_special_chars(text):
        '''
        Replace special chars
        '''
        for ch in ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '>', '#', '+', '-', '.', '!', '$', '\'', ':', '(', ')', '/']:
            if ch in text:
                text = text.replace(ch, "")

        return text

    @staticmethod
    def unquote_file(file):
        '''
        Function to uquote a file string from a url
        @file: file url string to unquote
        @return: file unquoted
        '''
        return f"/{unquote(file)}"

    @staticmethod
    def hash_password(password):
        '''
        Function that hash a password with a given salt
        @password: user plain-text password
        @return: password hashed in bytes. It contains the salt.
        '''
        return bcrypt.hashpw(password, bcrypt.gensalt())

    @staticmethod
    def check_password(plain_text_password, hashed_password):
        '''
        Function to compare two passowrds
        @plain_text_password: plain text password entered by a user
        @hashed_password: password retrived from database for a given user
        @return: bool. Result of comparisition.
        '''
        return bcrypt.checkpw(plain_text_password, hashed_password)
