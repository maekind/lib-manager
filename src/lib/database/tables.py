#!/usr/bin/env python3
'''
Database tables definition
'''

class Tables:
    """
    Class containing all table objects
    """

    def __init__(self, database):
        self._songs = database.classes.songs
               

    @property
    def songs(self):
        return self._songs

    @property
    def songs_name(self):
        return self._convert_name(self._songs)
    
    @staticmethod
    def _convert_name(table):
        return str(table).split(".")[3][:-2]
