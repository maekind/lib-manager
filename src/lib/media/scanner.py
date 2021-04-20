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

    def scan(self):
        '''
        Function to launch scan
        @return: tuple of list of Song, processed files and elapsed time
        '''
        songs = []
        start_time = time.time()
        
        # Iterate each element of the folder
        for root, subdirs, files in walk(self._folder):
            for fil in files:
                # If file is an accepted audio format then:
                if Path(fil).suffix in FORMAT_TYPES:
                    # Get tags from file
                    song = Tags.get_tags_from_file(path.join(root, fil))
                    # Adds song to the list
                    songs.append(song)
                    self._count += 1
                    
        total_time = time.time() - start_time
        return (songs, self._count, total_time)





