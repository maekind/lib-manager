# encoding:utf-8
'''
Spotify wrapper
'''
import base64
import urllib
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from fuzzywuzzy import process


__author__ = 'Marco Espinosa'
__version__ = '1.0'
__email__ = 'hi@marcoespinosa.com'


class Spotify:
    '''
    Class to get artist and album data from spotify
    A client id and a client secret tokens are necessary
    '''

    RATIO_MIN = 80

    @staticmethod
    def get_album_image(album_name, artist_name, default_image, client_id='70a5e19762ea4ae896e96756760d87ff', client_secret='67f055645e314dfb914854f7d7ed92ca'):
        '''
        Function that returns album image
        @album_name: album name to search
        @artist_name: artist name to search
        @return: base 64 album image or None
        '''
        try:

            client_credentials_manager = SpotifyClientCredentials(
                client_id=client_id, client_secret=client_secret)

            # spotify object to access API
            sp = spotipy.Spotify(
                client_credentials_manager=client_credentials_manager)

            # Search artist query
            result = sp.search(artist_name, type='artist')
            # Extract Artist's uri
            artist_uri = result['artists']['items'][0]['uri']

            # Store artist's albums' names' and uris in separate lists
            sp_albums = sp.artist_albums(artist_uri, album_type='album')

            # Extract album information
            album_names = []
            album_names.extend(sp_albums['items'])
            while sp_albums['next']:
                sp_albums = sp.next(sp_albums)
                album_names.extend(sp_albums['items'])

            # Sort albums
            album_names.sort(key=lambda album: album['name'].lower())

            # Create dictionary with results (name: image)
            album_dict = {}

            for album in album_names:
                name = album['name']
                image = album['images']
                url_image = image[1]['url']  # get size of 300
                album_dict.update({name: url_image})

            #print(json.dumps(album_dict, indent=4, sort_keys=True))

            sp_compilations = sp.artist_albums(
                artist_uri, album_type='compilation')

            # Extract album information
            compilations = []
            compilations.extend(sp_compilations['items'])
            while sp_compilations['next']:
                sp_compilations = sp.next(sp_compilations)
                compilations.extend(sp_compilations['items'])

            # Sort compilations
            compilations.sort(key=lambda album: album['name'].lower())

            for compilation in compilations:
                name = compilation['name']
                image = compilation['images']
                url_image = image[0]['url']
                album_dict.update({name: url_image})

            #print(json.dumps(album_dict, indent=4, sort_keys=True))

            # Search for album
            url_image = None
            album_name_list = []
            for album in album_dict:
                album_name_list.append(album)
            #print(album_name_list)
            Ratios = process.extract(
                album_name, album_name_list, limit=len(album_name_list))
            #print(Ratios)
            # You can also select the string with the highest matching percentage
            highest = process.extractOne(album_name, album_name_list)
            #print(highest)

            if highest[0] is not None:
                url_image = album_dict[highest[0]]

            if highest[1] > Spotify.RATIO_MIN:
                if url_image is not None:
                    image = urllib.request.urlopen(url_image).read()
                    # with open(f'/srv/music/images/albums/{album_name}.jpeg', "bw") as fil:
                    #     fil.write(image)
                    return base64.b64encode(image)
            else:
                print(f"RATIO: {highest[1]}")
        except Exception as ex:
            print(f"ERROR SPOTIFY: {ex}")

        return base64.b64encode(default_image)
        # return 0

# if __name__ == "__main__":
#     artist_name = "Queen"
#     album_name = "The Platinum Collection (CD 3)"

#     image = Spotify.get_album_image(album_name, artist_name)
#     if image != 0:
#         print("Image found!")
#     else:
#         print("Image not found!")
