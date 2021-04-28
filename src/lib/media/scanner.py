#!/usr/bin/env python3 
'''
Scanner file
'''
import time
from pathlib import Path
from os import walk, path
from lib.media.definitions import FORMAT_TYPES
from lib.media.song import Song
from lib.media.tags import Tags
from lib.media.spotify import Spotify

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

    def scan(self, database):
        '''
        Function to launch scan
        @return: tuple of list of Song, processed files and elapsed time
        '''
        songs = []
        start_time = time.time()

        # TODO: Get tokens from database and pass as parameter
        # token, expire = Spotify.get_token()
        # expired_time = start_time

        # Iterate each element of the folder
        for root, subdirs, files in walk(self._folder):
            for fil in files:
                # If file is an accepted audio format then:
                if Path(fil).suffix in FORMAT_TYPES:
                    # Check fot token expired time.
                    # If time expired, renew token.
                    # elapsed_time = time.time() - expired_time
                    # if elapsed_time >= expire:
                    #     token, expire = Spotify.get_token()
                    #     expired_time = time.time()
                    #     print("Token renewed")

                    #song = Tags.get_tags_from_file(path.join(root, fil), token)
                    song = Tags.get_tags_from_file(path.join(root, fil))
                    print(f"Got: {song.album} - {song.title}")
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
        print(f"Got: {song.album} - {song.title}")

        songs.append(song)
        id = database.add_song(song)
        total_time = time.time() - start_time
        return (songs, None, total_time)


