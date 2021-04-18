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
        @return: list of Song
        '''
        songs = []
        # start_time = time.time()
        first = True

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
                    # print(f'Processed files {self._count}', end='\r')
                    # if self._count == 1000:
                    #     print()
                    #     print("--- %s seconds ---" % (time.time() - start_time))
                    
        # print()
        # print("--- %s seconds ---" % (time.time() - start_time))
        return (songs, self._count)


if __name__ == "__main__":
    scanner = Scanner("/srv/music")
    songs, count = scanner.scan()
    print(f'Processed files: {count}')





