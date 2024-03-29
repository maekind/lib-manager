# encoding:utf-8
'''
Tags file
'''
import re
import urllib
import json
import base64
import io
import requests
from tinytag import TinyTag
from lib.utils import Utils
from lib.media.song import Song
from lib.media.spotify import Spotify
from lib.database.connector import Db


__author__ = 'Marco Espinosa'
__version__ = '1.0'
__email__ = 'hi@marcoespinosa.com'


class Tags:
    '''
    Class to fetch tags from an audio file
    '''

    @staticmethod
    def get_tags_from_file(file, default_image):
        '''
        Function that extract audio file information
        @file: audio file path.
        @return: A Song instance with audio information.
        '''
        # Fetch file information
        tag = TinyTag.get(file, image=True)

        # Initialize db connector
        database = Db()

        # Saving information into a Song instance
        song = Song()

        song.album = Utils.format_string(tag.album)
        song.album_artist = Utils.format_string(tag.albumartist)
        song.artist = Utils.format_string(tag.artist)
        song.duration = tag.duration if tag.duration is not None else 0
        song.genre = Utils.format_string(tag.genre)
        song.title = Utils.format_string(tag.title)
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
        song.artist_image = 0
        song.artist_image_fanart = 0
        song.album_image = 0
        if not database.artist_exists(song.artist):
            print("Getting image from TheAudioDB")
            artist_image, artist_image_fanart = Tags.fetch_artist_images(
                song.artist, default_image)
            song.artist_image = artist_image if not None else 0
            song.artist_image_fanart = artist_image_fanart if not None else 0
            print("Got image from TheAudioDB!")

        # Try to get album image from spotify, if token is provided
        if not database.album_exists(song.album) and song.album != "Unknown":
            print("Getting image from spotify")
            song.album_image = Spotify.get_album_image(
                song.album, song.artist, default_image)
            print("Got image from spotify!")

        return song

    @staticmethod
    def fetch_artist_images(artist, default_image):
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
            # print("TheAudioDB artist search ...")
            request = requests.get(url)
            data = json.load(request.content)
            # print("Done!")
            # Get artist image
            url_artist_image = data["artists"][0]["strArtistThumb"]

            if url_artist_image is not None:
                # Fetch artist image thumbnail
                # print("TheAudioDB getting artist image ...")
                response = requests.get(url_artist_image)
                image_bytes = io.BytesIO(response.content)
                artist_image = base64.b64encode(image_bytes)
                # print("Done!")
        except Exception:

            artist_image = base64.b64encode(default_image)

        try:
            # Get artist fan art image
            url_artist_image_fanart = data["artists"][0]["strArtistFanart"]

            if url_artist_image_fanart is not None:
                # Fetch artist image fan art
                # print("TheAudioDB getting artist fanart image ...")
                response = requests.get(url_artist_image_fanart)
                image_bytes = io.BytesIO(response.content)
                artist_image_fanart = base64.b64encode(image_bytes)
                # print("Done!")
        except Exception:

            artist_image_fanart = base64.b64encode(default_image)

        return (artist_image, artist_image_fanart)
