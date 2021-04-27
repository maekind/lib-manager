#!/usr/bin/env python3
'''
Tags file
'''
import re
import urllib
import json
import base64
from lib.utils import Utils
from urllib.parse import quote
from urllib.request import urlopen, Request
from os import path
from pathlib import Path
from tinytag import TinyTag
from lib.media.song import Song
from lib.media.spotify import Spotify


class Tags:
    '''
    Class to fetch tags from an audio file
    '''

    @staticmethod
    def get_tags_from_file(file, token=None):
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
        song.title = tag.title if tag.title is not None and tag.title != "" else "Unknown"
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

        # Images in base64
        artist_image, artist_image_fanart = Tags.fetch_artist_images(
            song.artist)
        song.artist_image = artist_image if not None else 0
        song.artist_image_fanart = artist_image_fanart if not None else 0
        
        # TODO: Implement spotify interface
        # Try to get album image from spotify, if token is provided
        # if token is not None and song.album != "Unknown":
        #     song.album_image = Spotify.get_album_image(token, song.album, song.artist) if not None else 0
        # else:
        song.album_image = 0

        return song



    @staticmethod
    def fetch_artist_images(artist):
        '''
        Tries to fetch album image from TheAudioDB and
        returns the image in base64 for database storage.
        '''
        artist_url = urllib.parse.quote_plus(artist)
        url = f"https://www.theaudiodb.com/api/v1/json/1/search.php?s={artist_url}"

        artist_image = None
        artist_image_fanart = None

        try:
            # Get artist json data
            request = urllib.request.urlopen(url)
            data = json.load(request)

            # Get artist image
            url_artist_image = data["artists"][0]["strArtistThumb"]

            if url_artist_image is not None:
                # Fetch artist image thumbnail
                artist_image = urllib.request.urlopen(url_artist_image).read()
                artist_image = base64.b64encode(artist_image)

        except Exception:

            artist_image = base64.b64encode(Utils.get_default_image())

        try:
            # Get artist fan art image
            url_artist_image_fanart = data["artists"][0]["strArtistFanart"]

            if url_artist_image_fanart is not None:
                # Fetch artist image fan art
                artist_image_fanart = urllib.request.urlopen(
                    url_artist_image_fanart).read()
                artist_image_fanart = base64.b64encode(artist_image_fanart)

        except Exception:

            artist_image_fanart = base64.b64encode(Utils.get_default_image())

        return (artist_image, artist_image_fanart)

    
