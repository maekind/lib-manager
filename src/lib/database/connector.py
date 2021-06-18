# encoding:utf-8
'''
Database interface
'''
import os
import mysql.connector
from mysql.connector import errorcode
from lib.media.song import Song
from lib.media.definitions import DATABASE
from lib.database.tables import TABLES_CREATE, TABLES_DROP, QUERIES, VIEWS_DROP, VIEWS_CREATE
from lib.logger import Logger
from lib.utils import Utils

__author__ = 'Marco Espinosa'
__version__ = '1.0'
__email__ = 'hi@marcoespinosa.com'


class Db:
    '''
    Handles database actions
    '''

    def __init__(self):
        '''
        Default constructor
        '''
        self._user = os.environ['DB_USER']
        self._password = os.environ['DB_PASSWORD']
        self._host = os.environ['DB_HOST']
        self._port = os.environ['DB_PORT']
        self._logger = Logger("database")
        self._database = DATABASE
        self._connection = None

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

            if freshdb:  # Delete previous structure
                self._logger.info("Initialising a fresh database ...")
               # Delete views
                for view_name in VIEWS_DROP:
                    self._logger.info(f"Dropping view {view_name}")
                    drop_query = f"DROP VIEW {view_name}"
                    try:
                        cursor.execute(drop_query)

                    except mysql.connector.Error as err:
                        self._logger.error(err.msg)
                    else:
                        self._logger.info(
                            f"View {view_name} dropped successfully.")

              # Delete tables
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
                self._logger.info("Initialising database ...")

            # Create tables
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

            # Create views
            for views_name in VIEWS_CREATE:
                view_description = VIEWS_CREATE[views_name]
                try:
                    self._logger.info(f"Creating view {views_name}...")
                    cursor.execute(view_description)
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        self._logger.error(
                            f"View {views_name} already exists: nothing to do.")
                    else:
                        self._logger.error(err.msg)
                else:
                    self._logger.info(
                        f"View {views_name} created successfully.")

           # Initialize content
            for query in QUERIES:
                query_description = QUERIES[query]
                try:
                    self._logger.info(f"Inserting data {query}...")
                    cursor.execute(query_description)
                    self._connection.commit()
                except mysql.connector.Error as err:
                    self._logger.error(err.msg)
                except Exception as err:
                    self._logger.error(err)
                else:
                    self._logger.info(
                        f"Data {query} inserted successfully.")

            cursor.close()
            self._connection.close()

            # Create admin login
            # TODO: only for testing purpouses
            username = "admin@admin.com"
            if not self.__user_exists(username):

                self.__connect()

                cursor = self._connection.cursor()

                sql_insert_login_query = """ INSERT INTO login
                            (name, email, password) VALUES (%s,%s,%s)"""

                password = "12345678"

                sql_insert_login_tuple = (
                    "admin", username, Utils.hash_password(password.encode('utf-8')))

                cursor.execute(sql_insert_login_query, sql_insert_login_tuple)
                self._connection.commit()
                cursor.close()
                self._connection.close()

            self._logger.info("Database initialized successfully.")

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

    def valid_login(self, username, password):
        '''
        Function to valid a username/password login
        @username: user name
        @password: user passowrd
        @return a boolean variable indicating wheather the username and password exist or not
        '''
        self._logger.info(f"Checking for login: {username}/{password}")
        res = None
        query = (f"SELECT password FROM login WHERE email = '{username}'")

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query)
            res = cursor.fetchone()

            cursor.close()
            self._connection.close()

            # Check for results
            if res is not None:
                db_password = res[0]

                # if hashed passwords are equal
                if Utils.check_password(password.encode('utf-8'), db_password):
                    return True

        return False

    def album_exists(self, album):
        '''
        Check the existance of an album in the database
        @album: album name
        @return: bool. wheather the album exist.
        '''
        result_id = None
        album = album.replace("'", "\\'")
        query = (f"SELECT id FROM album WHERE name = '{album}'")

        res = False

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query)
            result_id = cursor.fetchone()

            cursor.close()
            
            if result_id is not None:
                res = True

        self._connection.close()

        return res

    def artist_exists(self, artist):
        '''
        Check the existance of an artist in the database
        @artist: artist name
        @return: bool. wheather the artist exist.
        '''
        result_id = None
        artist = artist.replace("'", "\\'")
        query = (f"SELECT id FROM artist WHERE name = '{artist}'")

        res = False

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query)
            result_id = cursor.fetchone()

            cursor.close()
            
            if result_id is not None:
                res = True

        self._connection.close()

        return res

    def get_albums_data(self):
        '''
        Function to fetch albums data
        @return: database result
        '''
        query = ("SELECT * FROM albums_info_by_artist_album")

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query)
            data = []
            for (artist_name, album_name, duration, tracks, album_image) in cursor:
                data_dict = {}
                data_dict.update({"album_name": album_name})
                data_dict.update({"artist_name": artist_name})
                data_dict.update({"duration": duration})
                data_dict.update({"tracks": tracks})
                data_dict.update({"album_image_b64": str(album_image)})

                data.append(data_dict)

            cursor.close()
            

        self._connection.close()
        album_dict = {}
        album_dict.update({"albums": data})

        return album_dict

    def get_library_status(self):
        '''
        Function to get library status
        @return: database result
        '''
        query = ("SELECT lib_manager FROM status")

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query)
            result = cursor.fetchone()

            cursor.close()

        self._connection.close()

        return result[0]

    def set_library_status(self, status):
        '''
        Function to set library status
        @return: database result
        '''
        query = f"UPDATE status set lib_manager='{status}'"
        result = 0
        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()
            try:
                cursor.execute(query)
                self._connection.commit()

                cursor.close()

                # Check for update 
                query = f"SELECT lib_manager FROM status where lib_manager='{status}'"
                cursor = self._connection.cursor()
                cursor.execute(query)
                result = cursor.fetchone()

                result = len(result)

            except mysql.connector.errors.IntegrityError:
                self._logger.error(f"Integrity error: status type {status} does not exist!")
                result = -1

            self._connection.close()

        return result

    ############## PRIVATE METHODS ##############

    def __user_exists(self, username):
        '''
        Function to check if a username already exists
        @username: user name
        @return: bool. The result.
        '''
        self._logger.info(f"Checking for username existance ...")
        res = None
        query = (f"SELECT id FROM login WHERE email = '{username}'")

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query)
            res = cursor.fetchone()

            cursor.close()
            self._connection.close()

            # Check for results
            if res is not None:
                return True

        self._logger.error(f"User {username} exists!")
        self._connection.close()

        return False

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
        result_id = None
        title = song.title.replace("'", "\\'")
        query = (f"SELECT id FROM songs WHERE title = '{title}'")

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query)
            result_id = cursor.fetchone()

            if result_id is None:
                sql_insert_blob_query = """ INSERT INTO songs
                            (title, duration, track, file_id, album_id, artist_id) 
                            VALUES (%s,%s,%s,%s,%s,%s)"""
                insert_blob_tuple = (
                    title, song.duration, song.track, file_id, album_id, artist_id)
                cursor.execute(sql_insert_blob_query, insert_blob_tuple)
                self._connection.commit()
                result_id = cursor.lastrowid

            else:
                result_id = result_id[0]

            cursor.close()
            self._connection.close()

        return result_id

    def __add_file(self, song):
        '''
        Function to get the file id related to a file
        @song: song data
        @return: id
        '''
        # Select file id from file
        # If it doesn't exist, we added and fetch id.
        result_id = None
        audio_file = song.audio_file.replace("'", "\\'")
        query = (f"SELECT id FROM files WHERE path = '{audio_file}'")

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query)
            result_id = cursor.fetchone()

            if result_id is None:

                query = (
                    f"INSERT INTO files (path) VALUES ('{audio_file}')")

                cursor.execute(query)
                self._connection.commit()
                result_id = cursor.lastrowid

            else:
                result_id = result_id[0]

            cursor.close()
            self._connection.close()

        return result_id

    def __add_artist(self, song):
        '''
        Function to get the artist id related to an artist
        @song: song data
        @return: id
        '''
        # Select artist id from artist
        # If it doesn't exist, we added and fetch id.
        result_id = None
        artist = song.artist.replace("'", "\\'")
        query = (f"SELECT id FROM artist WHERE name = '{artist}'")

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query)
            result_id = cursor.fetchone()

            if result_id is None:
                sql_insert_blob_query = """ INSERT INTO artist
                          (name, image, image_fanart) VALUES (%s,%s,%s)"""
                insert_blob_tuple = (
                    artist, song.artist_image, song.artist_image_fanart)

                cursor.execute(sql_insert_blob_query, insert_blob_tuple)

                self._connection.commit()
                result_id = cursor.lastrowid

            else:
                result_id = result_id[0]

            cursor.close()
            self._connection.close()

        return result_id

    def __add_album(self, song, artist_id):
        '''
        Function to get the album id related to an album
        @song: song data
        @artist_id: artist id
        @return: id
        '''
        # Select album id from album
        # If it doesn't exist, we added and fetch id.

        result_id = None
        album = song.album.replace("'", "\\'")
        query = (f"SELECT id FROM album WHERE name = '{album}'")

        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()

            cursor.execute(query)
            result_id = cursor.fetchone()

            if result_id is None:
                sql_insert_blob_query = """ INSERT INTO album
                          (name, genre, tracks, year, image, artist_id) 
                          VALUES (%s,%s,%s,%s,%s,%s)"""
                insert_blob_tuple = (
                    album, song.genre, song.track_total, song.year, song.album_image, artist_id)

                cursor.execute(sql_insert_blob_query, insert_blob_tuple)

                self._connection.commit()
                result_id = cursor.lastrowid

            else:
                result_id = result_id[0]

            cursor.close()
            self._connection.close()

        return result_id
