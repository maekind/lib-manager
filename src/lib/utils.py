#!/usr/bin/env python3
'''
Utils functions
'''

from os import path
from pathlib import Path

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