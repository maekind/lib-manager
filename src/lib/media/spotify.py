#!/usr/bin/env python3
'''
Spotify wrapper
'''
import requests
import base64
import json
import urllib
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from os import path
from pathlib import Path
from urllib.request import urlopen
from lib.utils import Utils

class Spotify:
    '''
    Class to get artist and album data from spotify
    A client id and a client secret tokens are necessary
    '''

    # TODO: delete clientId and clientSecret values.
    @staticmethod
    def get_token(client_id='70a5e19762ea4ae896e96756760d87ff', client_secret='67f055645e314dfb914854f7d7ed92ca'):
        '''
        Function that gets an available token for searches
        @client_id: spotify client id
        @client_secret: spotify client secret
        @return: tuple of (token, expiration time)
        '''
        url = "https://accounts.spotify.com/api/token"
        headers = {}
        data = {}

        # Encode as Base64
        message = f"{client_id}:{client_secret}"
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')


        headers['Authorization'] = f"Basic {base64_message}"
        data['grant_type'] = "client_credentials"

        r = requests.post(url, headers=headers, data=data)

        token = r.json()['access_token']
        expires = r.json()['expires_in']
        
        return (token, expires)


    @staticmethod
    def get_album_image(token, album_name, artist_name, client_id='70a5e19762ea4ae896e96756760d87ff', client_secret='67f055645e314dfb914854f7d7ed92ca'):
        '''
        Function that returns album image
        @token: spotify token
        @album_name: album name to search
        @return: base 64 album image or None
        '''
        # image = None

        # album_name = Utils.replace_special_chars(album_name)

        # album_url = f"https://api.spotify.com/v1/search?q={album_name}&type=album&limit=1"

        # headers = {
        #     "Authorization": "Bearer " + token
        # }

        # album_url = "https://api.spotify.com/v1/artists/7bu3H8JO7d0UbMoVzbo70s"
        # res = requests.get(url=album_url, headers=headers)

        # res_json = res.json()
        # print(res_json)

        # try:
        #     image_height = 0
        #     image_url = None
        #     for image_item in res_json["albums"]["items"][0]["images"]:
        #         if image_item["height"] > image_height:
        #             image_height = image_item["height"]
        #             image_url = image_item["url"]
            
        #     if image_url is not None:
        #         image = urllib.request.urlopen(image_url).read()

        # except Exception as ex:
        #     print(f"Error: {ex}")
        #     image = Utils.get_default_image()

        # if image is not None:
        #     with open(f'/srv/music/images/albums/{album_name}.jpeg', "bw") as fil:
        #         fil.write(image)
        #     return base64.b64encode(image)
        
        # return 0

        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API
        print(artist_name)
        result = sp.search(artist_name) #search query
        #result['tracks']['items'][0]['artists']
        #Extract Artist's uri
        artist_uri = result['tracks']['items'][0]['artists'][0]['uri']#Pull all of the artist's albums
        sp_albums = sp.artist_albums(artist_uri, album_type='album')#Store artist's albums' names' and uris in separate lists
        # album_names = []
        # album_uris = []
        # for i in range(len(sp_albums['items'])):
        #     album_names.append(sp_albums['items'][i]['name'])
        #     album_uris.append(sp_albums['items'][i]['uri'])
            
        # album_names
        # album_uris
        print(sp_albums)

# if __name__ == "__main__":
#     token, expires = Spotify.get_token()
#     album_name = "The fellowship of the Ring"

#     image = Spotify.get_album_image(token, album_name)
#     if image is not None:
#         with open('./image.jpeg', "bw") as fil:
#             fil.write(image)


