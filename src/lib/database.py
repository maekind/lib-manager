#!/usr/bin/env python3 
'''
Database interface
'''
import os
from song import Song

class Db:
    '''
    Handles database actions
    '''

    def __init__(self):
        '''
        Default constructor
        '''
        self.username = os.environ['DB_USER']
        self.password = os.environ['DB_PASSWORD']
        self.host = os.environ['DB_HOST']
        self.port = os.environ['DB_PORT']

    def get_path_file(id):
        '''
        Returns the path file for a given id
        @id: id field
        @return: path file string
        '''

    def insert(song):
        '''
        Inserts a song into the database
        @song: song information
        @return: result
        '''

    def delete(song_file):
        '''
        Deletes a song from the database
        @song_file: song local file
        @return: result
        '''



