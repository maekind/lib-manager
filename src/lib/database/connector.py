#!/usr/bin/env python3
'''
Database interface
'''

import os
import mysql.connector
from mysql.connector import errorcode
from lib.media.song import Song
from lib.media.definitions import DATABASE
from lib.database.tables import TABLES


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

    def init_db(self):
        '''
        Initialize database: tables creation
        '''
        self._logger.info(f"Initialising database...")
        self.__connect()
        if self._connection is not None:
            cursor = self._connection.cursor()
            for table_name in TABLES:
                table_description = TABLES[table_name]
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
