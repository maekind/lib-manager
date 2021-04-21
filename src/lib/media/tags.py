#!/usr/bin/env python3 
'''
Tags file
'''
import re
from tinytag import TinyTag
from lib.media.song import Song

class Tags:
    '''
    Class to fetch tags from an audio file
    '''

    @staticmethod
    def get_tags_from_file(file):
        '''
        Function that extract audio file information
        @file: audio file path.
        @return: A Song instance with audio information.
        '''
        # Fetch file information
        tag = TinyTag.get(file, image=True)
        
        # Saving information into a Song instance
        song = Song()
        song.album = tag.album if tag.album is not None else "Not known"
        song.albumartist = tag.albumartist if tag.albumartist is not None else "Not known"
        song.artist = tag.artist if tag.artist is not None else "Not known"
        song.duration = tag.duration if tag.duration is not None else 0
        song.genre = tag.genre if tag.genre is not None else "Not known"
        song.album_image = tag.get_image()
        song.artist_image = tag.get_image()
        song.title = tag.title if tag.title is not None else "Not known"
        song.track = tag.track if tag.track is not None else 0
        song.track_total = tag.track_total if tag.track_total is not None else 0
        if tag.year is not None and tag.year != "":
            song.year = tag.year if len(str(tag.year)) == 4 else str(tag.year)[:4]
            expr = "^[0-9]+$"
            if not re.search(expr, song.year):
                song.year = 0            
        else:
            song.year = 0
            
        song.audio_file = file
        
        return song

    @staticmethod
    def fetch_album_image(album):
        '''
        Tries to fetch album image from TheAudioDB and
        returns the image in base64 for database storage.
        '''
        url = ""
        # TODO: I don't from where ...

    @staticmethod
    def fetch_artist_image(artist):
        '''
        Tries to fetch album image from TheAudioDB and
        returns the image in base64 for database storage.
        '''
        url = f"https://www.theaudiodb.com/api/v1/json/1/search.php?s={artist}"
        # TODO: send a request


        