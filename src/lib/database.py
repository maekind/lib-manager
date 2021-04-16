#!/usr/bin/env python3 
'''
Database interface
'''
import sys
import os
from pathlib import Path
from lib.song import Song
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database

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
        self._database = "music"
               
        self._engine = create_engine(
            "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(self._user, self._password, self._host, self._port, self._database)
        )

        logger.debug(f"ConnectionString: mysql://{self._user}:{self._password}@{self._host}:{self._port}/{self._database}")

    def session(self):
        """
        Start a new transaction on the established database connection.
        """
        self._base = automap_base()
        self._base.prepare(self._engine, reflect=True)

        self._sessionmaker = sessionmaker(bind=self._engine)
        return self._sessionmaker

    def connect(self, dbname):
        '''
        Function to connect to a database
        '''
        # self.base = automap_base()
        # self.engine = create_engine(
        #     "mysql://{0}:{1}@{2}:{3}/{4}".format(self._user, self._password, self._host, self._port, dbname)
        # )
        # self.base.prepare(self.engine, reflect=True)

        # self._sessionmaker = sessionmaker(bind=self.engine)

    @property
    def classes(self):
        """
        Forward requests for relationship classes to the base.
        """
        return self.base.classes

    def get_path_file(self, id):
        '''
        Returns the path file for a given id
        @id: id field
        @return: path file string
        '''

    def insert(self, song):
        '''
        Inserts a song into the database
        @song: song information
        @return: result
        '''

    def delete(self, song_file):
        '''
        Deletes a song from the database
        @song_file: song local file
        @return: result
        '''

    def __sql_files_in(self, folder):
        '''
        Returns an alphabetically sorted list of files ending in '.sql' in
        the specified folder.
        '''
        sql_files = [
            os.path.join(r, filename)
            for r, _, f in os.walk(folder)
            for filename in f
            if filename.endswith(".sql")
        ]

        return sorted(sql_files)

    def init_db(self):
        '''
        Function to create database if it does not exist
        '''
        if database_exists(self._engine.url):
            self._logger.info(f"Running tables initialization ...")
            
            for sql_file in self.__sql_files_in(Path(__file__).resolve().parent.parent / "conf"):
                self._logger.info(f"Running {Path(sql_file).name}")
                with self._engine.begin() as conn:
                    with open(sql_file, "br") as ddl:
                        conn.execute(ddl.read().decode("utf-8-sig", "ignore"))

            with self._engine.connect() as connection:
                result = connection.execute(text("insert into temp values (1,'ttttt')"))
                result = connection.execute(text("select field1 from temp"))
                for row in result:
                    self._logger.debug("Field 1 content: ", row['field1'])

            self._logger.info(f"Initialization complete successfully")
            return True
        else:
            self._logger.info("Databse already exists; doing nothing!")
            return False   
        


