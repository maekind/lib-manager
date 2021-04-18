#!/usr/bin/env python3 
'''
Tags file
'''
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
        song.album = tag.album
        song.albumartist = tag.albumartist
        song.artist = tag.artist
        song.duration = tag.duration
        song.genre = tag.genre
        song.image = tag.get_image()
        song.title = tag.title
        song.track = tag.track
        song.track_total = tag.track_total
        song.year = tag.year
        song.audio_file = file
        
        return song
        