#!/usr/bin/env python3
'''
Database interface
'''

import os
import mysql.connector
from mysql.connector import errorcode
from lib.media.song import Song
from lib.media.definitions import DATABASE
from lib.database.tables import TABLES_CREATE


class Db:
    '''
    Handles database actions
    '''

    def __init__(self, logger):
        '''
        Default constructor
        '''
        self._user = os.environ['DB_USER']
        self._password = os.environ['DB_PASSWORD']
        self._host = os.environ['DB_HOST']
        self._port = os.environ['DB_PORT']
        self._logger = logger
        self._database = DATABASE

    def __connect(self):
        '''
        Function to connect to database
        '''
        try:
            self._connection = mysql.connector.connect(user=self._user, password=self._password,
                                                       host=self._host,
                                                       database=self._database)

        except mysql.connector.Error as err:

            self._connection = None

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self._logger.error(
                    "Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self._logger.error("Database does not exist")
            else:
                self._logger.error(err)

    def init_db(self, freshdb):
        '''
        Initialize database: tables creation
        @freshdb: Weather the daabase instance has to be new.
        '''
        self._logger.info(f"Initialising database...")
        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            for table_name in TABLES_CREATE:
                table_description = TABLES_CREATE[table_name]
                try:
                    self._logger.info(f"Creating table {table_name}...")
                    cursor.execute(table_description)
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        self._logger.error(
                            "Table {table_name} already exists: nothing to do.")
                    else:
                        self._logger.error(err.msg)
                else:
                    self._logger.info(
                        f"Table {table_name} created successfully.")

            cursor.close()
            self._connection.close()

            self._logger.info(f"Database initialized successfully.")

    def add_song(self, song):
        '''
        Function to save song data into the database
        @song: song data
        '''
        # Every step only if it doesn't exist.
        # 1-Add file
        file_id = self.__add_file(song)
        # 2-Add artist
        artist_id = self.__add_artist(song)
        # 3-Add album
        album_id = self.__add_album(song, artist_id)
        # 4-Add song
        song_id = self.__add_song(song, file_id, artist_id, album_id)

        return song_id

    def __add_song(self, song, file_id, artist_id, album_id):
        '''
        Function to get the file id related to a file
        @song: song data
        @file_id: file id
        @artist_id: artist id
        @album_id: album id
        @return: id
        '''
        # Select file id from file
        # If it doesn't exist, we added and fetch id.
        id = None

        query = ("SELECT id FROM songs "
                 "WHERE name = %s")

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query, (song.title))
            id = cursor.fetchone()

            if id is None:
                query = ("INSERT INTO songs "
                         "(title, duration, track, file_id, album_id, artist_id) "
                         "VALUES (%s, %s, %s, %s, %s, %s)")
                cursor.execute(query, (song.title, song.duration,
                               song.track, file_id, album_id, artist_id))

                id = cursor.lastrowid

            self._connection.commit()
            cursor.close()
            self._connection.close()

        return id

    def __add_file(self, song):
        '''
        Function to get the file id related to a file
        @song: song data
        @return: id
        '''
        # Select file id from file
        # If it doesn't exist, we added and fetch id.
        id = None

        query = ("SELECT id FROM files "
                 "WHERE path = %s")

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query, (song.audio_file))
            id = cursor.fetchone()

            if id is None:
                query = ("INSERT INTO files "
                         "(path) "
                         "VALUES (%s)")
                cursor.execute(query, (song.audio_file))

                id = cursor.lastrowid
            
            self._connection.commit()
            cursor.close()
            self._connection.close()

        return id

    def __add_artist(self, song):
        '''
        Function to get the artist id related to an artist
        @song: song data
        @return: id
        '''
        # Select artist id from artist
        # If it doesn't exist, we added and fetch id.
        id = None

        query = ("SELECT id FROM artist "
                 "WHERE name = %s")

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query, (song.artist))
            id = cursor.fetchone()

            if id is None:
                query = ("INSERT INTO artist "
                         "(name, image) "
                         "VALUES (%s, %s)")
                cursor.execute(query, (song.artist, 'null'))

                id = cursor.lastrowid

            self._connection.commit()
            cursor.close()
            self._connection.close()

        return id

    def __add_album(self, song, artist_id):
        '''
        Function to get the album id related to an album
        @song: song data
        @artist_id: artist id
        @return: id
        '''
        # Select album id from album
        # If it doesn't exist, we added and fetch id.

        id = None

        query = ("SELECT id FROM album "
                 "WHERE name = %s")

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query, (song.album))
            id = cursor.fetchone()

            if id is None:
                query = ("INSERT INTO album "
                         "(name, genre, tracks, year, image, artist_id) "
                         "VALUES (%s, %s, %s, %s, %s, %s)")
                cursor.execute(query, (song.album, song.genre,
                               song.track_total, song.year, 'null', artist_id))

                id = cursor.lastrowid
            
            self._connection.commit()
            cursor.close()
            self._connection.close()

        return id
