#!/usr/bin/env python3
'''
Tags file
'''
import re
import urllib
import json
import base64
from urllib.parse import quote
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
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

        # Images in base64
        artist_image, artist_image_fanart = Tags.fetch_artist_images(song.artist)
        song.artist_image = artist_image if not None else 0
        song.artist_image_fanart = artist_image_fanart if not None else 0
        song.album_image = Tags.fetch_album_image(song.album) if not None else 0

        return song

    @staticmethod
    def fetch_album_image(album):
        '''
        Tries to fetch album image from google and
        returns the image in base64 for database storage.
        '''
        albumart = None
        try:
            album_search = album + " Album Art"
            url = ("https://www.google.com/search?q=" +
                quote(album_search.encode('utf-8')) + "&source=lnms&tbm=isch")
            header = {'User-Agent':
                    '''Mozilla/5.0 (Windows NT 6.1; WOW64)
                    AppleWebKit/537.36 (KHTML,like Gecko)
                    Chrome/43.0.2357.134 Safari/537.36'''
                    }

            soup = BeautifulSoup(urlopen(Request(url, headers=header)), "html.parser")
            albumart_div = soup.find("div", {"class": "rg_i"})
            print(albumart_div)
            albumart = base64.b64encode(json.loads(albumart_div.text)["ou"])

            with open(path.join("/srv/music/images/fanart", album + ".jpeg"), "bw") as fil:
                fil.write(json.loads(albumart_div.text)["ou"])

        except Exception as e:
            print(f"EROR: {e}")
            albumart = base64.b64encode(Tags.get_default_image())
            with open(path.join("/srv/music/images/fanart", album + ".jpeg"), "bw") as fil:
                fil.write(Tags.get_default_image())
        
        return albumart

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

            artist_image = base64.b64encode(Tags.get_default_image())

            
        try:
            # Get artist fan art image
            url_artist_image_fanart = data["artists"][0]["strArtistFanart"]

            if url_artist_image_fanart is not None:
                # Fetch artist image fan art
                artist_image_fanart = urllib.request.urlopen(url_artist_image_fanart).read()
                artist_image_fanart = base64.b64encode(artist_image_fanart)

        except Exception:
            
            artist_image_fanart = base64.b64encode(Tags.get_default_image())
            
        
        return (artist_image, artist_image_fanart)

    @staticmethod
    def get_default_image():
        '''
        Function to fetch the default image file for unknowms
        '''
        with open(Path(".").resolve() / path.join("lib", "media", "res", "unknown.jpeg"), "br") as image_file:
            image = image_file.read()
        
        return image
