#!/usr/bin/env python3
'''
Tags file
'''
import re
import urllib
import json
import base64
from os import path
from pathlib import Path
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
        song.album = tag.album if tag.album is not None else "Unknown"
        song.albumartist = tag.albumartist if tag.albumartist is not None else "Unknown"
        song.artist = tag.artist if tag.artist is not None else "Unknown"
        song.duration = tag.duration if tag.duration is not None else 0
        song.genre = tag.genre if tag.genre is not None else "Unknown"
        song.album_image = tag.get_image()
        song.title = tag.title if tag.title is not None else "Unknown"
        song.track = tag.track if tag.track is not None else 0
        song.track_total = tag.track_total if tag.track_total is not None else 0
        if tag.year is not None and tag.year != "":
            song.year = tag.year if len(
                str(tag.year)) == 4 else str(tag.year)[:4]
            expr = "^[0-9]+$"
            if not re.search(expr, song.year):
                song.year = 0
        else:
            song.year = 0

        song.audio_file = file

        artist_image = Tags.fetch_artist_image(song.artist)
        song.artist_image = artist_image if not None else 0

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
        artist_url = urllib.parse.quote_plus(artist)
        url = f"https://www.theaudiodb.com/api/v1/json/1/search.php?s={artist_url}"

        try:
            # Get artist json data
            request = urllib.request.urlopen(url)
            data = json.load(request)
            url_image = data["artists"][0]["strArtistThumb"]

            if url_image is not None:
                # Fetch image
                artist_image = urllib.request.urlopen(url_image).read()
                # Convert image to base 64 for storage base64.b64encode(
                return artist_image
                
        except Exception:
            #print("Getting image by default.")
            artist_image = None
            with open(Path(".").resolve() / path.join("lib", "media", "res", "unknown.jpeg"), "br") as image_file:
                artist_image = image_file.read()

            return artist_image
