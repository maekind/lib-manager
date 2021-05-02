# encoding:utf-8
'''
Database TABLES_CREATE and initializations
'''


__author__ = 'Marco Espinosa'
__version__ = '1.0'
__email__ = 'hi@marcoespinosa.com'


TABLES_CREATE = {}

QUERIES = {}

TABLES_CREATE['status_types'] = (
    "CREATE TABLE `status_types` ("
    "  `type` varchar(50),"
    "  PRIMARY KEY (`type`)"
    ") ENGINE=InnoDB")

TABLES_CREATE['status'] = (
    "CREATE TABLE `status` ("
    "  `lib_manager` varchar(200),"
    "  KEY `lib_manager` (`lib_manager`),"
    "  CONSTRAINT `status_ibfk_1` FOREIGN KEY (`lib_manager`) REFERENCES `status_types` (`type`)"
    ") ENGINE=InnoDB")

TABLES_CREATE['login'] = (
    "CREATE TABLE `login` ("
    "  `id` int unsigned NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(200) NOT NULL,"
    "  `avatar` mediumblob,"
    "  `email` varchar(200) NOT NULL,"
    "  `password` varchar(512) NOT NULL,"
    "  `spotify_client_id` varchar(128),"
    "  `spotify_client_secret` varchar(128),"
    "  `salt` varchar(128),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES_CREATE['configuration'] = (
    "CREATE TABLE `configuration` ("
    "  `id` int unsigned NOT NULL AUTO_INCREMENT,"
    "  `user_id` int unsigned NOT NULL,"
    "  `lib_path` varchar(512),"
    "  `language` varchar(25),"
    "  `spotify_client_id` varchar(128),"
    "  `spotify_client_secret` varchar(128),"
    "  PRIMARY KEY (`id`),"
    "  KEY `user_id` (`user_id`),"
    "  CONSTRAINT `configuration_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `login` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES_CREATE['artist'] = (
    "CREATE TABLE `artist` ("
    "  `id` int unsigned NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(200) NOT NULL,"
    "  `image` mediumblob,"
    "  `image_fanart` mediumblob,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")


TABLES_CREATE['album'] = (
    "CREATE TABLE `album` ("
    "  `id` int unsigned NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(100) NOT NULL,"
    "  `genre` varchar(100) DEFAULT NULL,"
    "  `tracks` int unsigned NOT NULL,"
    "  `year` int unsigned NOT NULL,"
    "  `image` mediumblob,"
    "  `artist_id` int unsigned NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  KEY `artist_id` (`artist_id`),"
    "  CONSTRAINT `album_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `artist` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")


TABLES_CREATE['files'] = (
    "CREATE TABLE `files` ("
    "  `id` int unsigned NOT NULL AUTO_INCREMENT,"
    "  `path` varchar(512) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")


TABLES_CREATE['songs'] = (
    "CREATE TABLE `songs` ("
    "  `id` int unsigned NOT NULL AUTO_INCREMENT,"
    "  `title` varchar(200) NOT NULL,"
    "  `duration` float unsigned NOT NULL,"
    "  `track` int unsigned NOT NULL,"
    "  `file_id` int unsigned NOT NULL,"
    "  `album_id` int unsigned NOT NULL,"
    "  `artist_id` int unsigned NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  KEY `album_id` (`album_id`),"
    "  KEY `artist_id` (`artist_id`),"
    "  KEY `file_id` (`file_id`),"
    "  CONSTRAINT `songs_ibfk_1` FOREIGN KEY (`album_id`) REFERENCES `album` (`id`) ON DELETE CASCADE,"
    "  CONSTRAINT `songs_ibfk_2` FOREIGN KEY (`artist_id`) REFERENCES `artist` (`id`) ON DELETE CASCADE,"
    "  CONSTRAINT `songs_ibfk_3` FOREIGN KEY (`file_id`) REFERENCES `files` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")


TABLES_CREATE['playlist'] = (
    "CREATE TABLE `playlist` ("
    "  `id` int unsigned NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(100) NOT NULL,"
    "  `genre` varchar(100) DEFAULT NULL,"
    "  `song_id` int unsigned NOT NULL,"
    "  `user_id` int unsigned NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  KEY `song_id` (`song_id`),"
    "  KEY `user_id` (`song_id`),"
    "  CONSTRAINT `playlist_ibfk_1` FOREIGN KEY (`song_id`) REFERENCES `songs` (`id`) ON DELETE CASCADE,"
    "  CONSTRAINT `playlist_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `login` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES_CREATE['starred_songs'] = (
    "CREATE TABLE `starred_songs` ("
    "  `id` int unsigned NOT NULL AUTO_INCREMENT,"
    "  `user_id` int unsigned NOT NULL,"
    "  `song_id` int unsigned NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  KEY `user_id` (`user_id`),"
    "  KEY `song_id` (`song_id`),"
    "  CONSTRAINT `starred_songs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `login` (`id`) ON DELETE CASCADE,"
    "  CONSTRAINT `starred_songs_ibfk_2` FOREIGN KEY (`song_id`) REFERENCES `songs` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES_CREATE['starred_albums'] = (
    "CREATE TABLE `starred_albums` ("
    "  `id` int unsigned NOT NULL AUTO_INCREMENT,"
    "  `user_id` int unsigned NOT NULL,"
    "  `album_id` int unsigned NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  KEY `user_id` (`user_id`),"
    "  KEY `album_id` (`album_id`),"
    "  CONSTRAINT `starred_albums_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `login` (`id`) ON DELETE CASCADE,"
    "  CONSTRAINT `starred_albums_ibfk_2` FOREIGN KEY (`album_id`) REFERENCES `album` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES_CREATE['statistics'] = (
    "CREATE TABLE `statistics` ("
    "  `id` int unsigned NOT NULL AUTO_INCREMENT,"
    "  `song_id` int unsigned NOT NULL,"
    "  `played` int unsigned NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  KEY `song_id` (`song_id`),"
    "  CONSTRAINT `statistics_ibfk_1` FOREIGN KEY (`song_id`) REFERENCES `songs` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES_DROP = ["status", "status_types", "configuration",
               "statistics", "starred_songs", "starred_albums",
               "playlist", "login", "songs", "album", "artist", "files"]

QUERIES["status_types"] = """ INSERT INTO status_types
                          (type) VALUES 
                          ('ERROR'),
                          ('PENDING'),
                          ('OK'),
                          ('NOT INIT'),
                          ('INIT') """

# 2021-04-18 19:34:53
