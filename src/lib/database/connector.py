#!/usr/bin/env python3
'''
Database interface
'''
import json
import os
import mysql.connector
import base64
from mysql.connector import errorcode
from lib.media.song import Song
from lib.media.definitions import DATABASE
from lib.database.tables import TABLES_CREATE, TABLES_DROP, QUERIES


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
        
        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            if freshdb:
                # Delete previous tables
                self._logger.info(f"Initialising a fresh database ...")
                for table_name in TABLES_DROP:
                    self._logger.info(f"Dropping table {table_name}")
                    drop_query = f"DROP TABLE {table_name}"
                    try:
                        cursor.execute(drop_query)
                    except mysql.connector.Error as err:
                        self._logger.error(err.msg)
                else:
                    self._logger.info(
                        f"Table {table_name} dropped successfully.")
            else:
                self._logger.info(f"Initialising database ...")


            for table_name in TABLES_CREATE:
                table_description = TABLES_CREATE[table_name]
                try:
                    self._logger.info(f"Creating table {table_name}...")
                    cursor.execute(table_description)
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        self._logger.error(
                            f"Table {table_name} already exists: nothing to do.")
                    else:
                        self._logger.error(err.msg)
                else:
                    self._logger.info(
                        f"Table {table_name} created successfully.")
            for query in QUERIES:
                query_description = QUERIES[query]
                try:
                    self._logger.info(f"Inserting data {query}...")
                    cursor.execute(query_description)
                    self._connection.commit()
                except mysql.connector.Error as err:
                    self._logger.error(err.msg)
                else:
                    self._logger.info(
                        f"Data {query} inserted successfully.")
            
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

    def delete_file(self, file):
        '''
        Function to delete a file from database
        @file: file path to delete
        @return: deleted records
        '''
        res = 0
        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()
            print(file)
            query = f"DELETE FROM files WHERE path = '{file}'"
            
            cursor.execute(query)
            res = cursor.rowcount
            self._connection.commit()
            cursor.close()
            self._connection.close()
        
        return res


    ############## PRIVATE METHODS ##############

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
        title = song.title.replace("'", "\\'")
        query = (f"SELECT id FROM songs WHERE title = '{title}'")
        
        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query)
            id = cursor.fetchone()
            
            if id is None:
                query = (f"INSERT INTO songs (title, duration, track, file_id, album_id, artist_id) VALUES ('{title}', {song.duration}, {song.track}, {file_id}, {album_id}, {artist_id})")
                cursor.execute(query)
                self._connection.commit()
                id = cursor.lastrowid
                
            else:
                id = id[0]

            
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
        audio_file = song.audio_file.replace("'", "\\'")
        query = (f"SELECT id FROM files WHERE path = '{audio_file}'")

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query)
            id = cursor.fetchone()
            
            if id is None:
                
                query = (
                    f"INSERT INTO files (path) VALUES ('{audio_file}')")
                
                cursor.execute(query)
                self._connection.commit()
                id = cursor.lastrowid
                
            else:
                id = id[0]
            
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
        artist = song.artist.replace("'", "\\'")
        query = (f"SELECT id FROM artist WHERE name = '{artist}'")

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query)
            id = cursor.fetchone()
            
            if id is None:
                sql_insert_blob_query = """ INSERT INTO artist
                          (name, image, image_fanart) VALUES (%s,%s,%s)"""
                insert_blob_tuple = (artist, song.artist_image, song.artist_image_fanart)

                cursor.execute(sql_insert_blob_query, insert_blob_tuple)
                
                self._connection.commit()
                id = cursor.lastrowid

            else:
                id = id[0]
            
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
        album = song.album.replace("'", "\\'")
        query = (f"SELECT id FROM album WHERE name = '{album}'")

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query)
            id = cursor.fetchone()
            
            if id is None:
                query = (f"INSERT INTO album (name, genre, tracks, year, artist_id) VALUES ('{album}', '{song.genre}', {song.track_total}, {song.year}, {artist_id})")
                
                cursor.execute(query)
                self._connection.commit()
                id = cursor.lastrowid
                
            else:
                id = id[0]
            
            cursor.close()
            self._connection.close()

        return id
