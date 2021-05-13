# encoding:utf-8
'''
Scanner file
'''
import time
from pathlib import Path
from os import walk, path
from lib.media.definitions import FORMAT_TYPES
from lib.media.tags import Tags
from lib.logger import Logger, Level

__author__ = 'Marco Espinosa'
__version__ = '1.0'
__email__ = 'hi@marcoespinosa.com'


class Scanner:
    '''
    Class to perform scanner actions into music folder
    to recreate the entire library
    '''

    def __init__(self, folder):
        '''
        Default constructor
        @folder: folder to scan
        '''
        self._folder = folder
        self._count = 0
        self._image = self.__get_default_image()
        
        # TODO: In production configure logger to info.
        self._logger = Logger("scanner", Level.DEBUG)

    def scan(self, database):
        '''
        Function to launch scan
        @return: tuple of list of Song, processed files and elapsed time
        '''
        songs = []
        start_time = time.time()

        # Iterate each element of the folder
        for root, subdirs, files in walk(self._folder):
            self._logger.debug(f"Checking into {root}")
            for fil in files:
                self._logger.debug(f"Checking for file {fil}")
                # If file is an accepted audio format then:
                if Path(fil).suffix in FORMAT_TYPES:
                    # TODO: Maybe check if file exists in database before launching get_tags!
                    # That would be speedy!
                    song = Tags.get_tags_from_file(path.join(root, fil), self._image)
                    self._logger.debug(f"Got: {song.artist} - {song.album} - {song.title}")
                    # Adds song to the list
                    songs.append(song)
                    id = database.add_song(song)
                    self._count += 1

        total_time = time.time() - start_time
        return (songs, self._count, total_time)

    def scan_file(self, file_path, database):
        '''
        Function to launch scan in one file
        @return: tuple of list of Song, processed files and elapsed time
        '''
        songs = []
        start_time = time.time()
        song = Tags.get_tags_from_file(file_path)
        self._logger.debug(f"Got: {song.album} - {song.title}")

        songs.append(song)
        id = database.add_song(song)
        total_time = time.time() - start_time
        return (songs, None, total_time)

    def __get_default_image(self):
        '''
        Function to fetch the default image file for unknowms
        '''
        with open(Path(".").resolve() / path.join("lib", "media", "res", "unknown.jpg"), "br") as image_file:
            image = image_file.read()

        return image
