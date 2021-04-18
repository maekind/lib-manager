#!/usr/bin/env python3 
'''
Song model file
'''

class Song:
    '''
    Class for song model
    '''

    def __init__(self):
        '''
        Default constructor
        '''
        

    @property
    def album(self):
        '''
        album property getter
        '''
        return self._album

    @album.setter
    def album(self, value):
        '''
        album property setter
        '''
        self._album = value

    @property
    def albumartist(self):
        '''
        albumartist property getter
        '''
        return self._albumartist

    @albumartist.setter
    def albumartist(self, value):
        '''
        albumartist property setter
        '''
        self._albumartist = value

    @property
    def artist(self):
        '''
        artist property getter
        '''
        return self._artist

    @artist.setter
    def artist(self, value):
        '''
        artist property setter
        '''
        self._artist = value

    @property
    def duration(self):
        '''
        duration property getter
        '''
        return self._duration

    @duration.setter
    def duration(self, value):
        '''
        duration property setter
        '''
        self._duration = value

    @property
    def genre(self):
        '''
        genre property getter
        '''
        return self._genre

    @genre.setter
    def genre(self, value):
        '''
        genre property setter
        '''
        self._genre = value

    @property
    def title(self):
        '''
        title property getter
        '''
        return self._title

    @title.setter
    def title(self, value):
        '''
        title property setter
        '''
        self._title = value

    @property
    def track(self):
        '''
        track property getter
        '''
        return self._track

    @track.setter
    def track(self, value):
        '''
        track property setter
        '''
        self._track = value

    @property
    def track_total(self):
        '''
        track_total property getter
        '''
        return self._track_total

    @track_total.setter
    def track_total(self, value):
        '''
        track_total property setter
        '''
        self._track_total = value

    @property
    def year(self):
        '''
        year property getter
        '''
        return self._year

    @year.setter
    def year(self, value):
        '''
        year property setter
        '''
        self._year = value

    @property
    def image(self):
        '''
        image property getter
        '''
        return self._image

    @image.setter
    def image(self, value):
        '''
        image property setter
        '''
        self._image = value

    @property
    def audio_file(self):
        '''
        audio_file property getter
        '''
        return self._audio_file

    @audio_file.setter
    def audio_file(self, value):
        '''
        audio_file property setter
        '''
        self._audio_file = value