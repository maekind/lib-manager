# Database TABLES_CREATE

TABLES_CREATE = {}

TABLES_CREATE['artist'] = (
    "CREATE TABLE `artist` ("
    "  `id` int unsigned NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(200) NOT NULL,"
    "  `image` mediumblob,"
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
    "  CONSTRAINT `album_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `artist` (`id`)"
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
    "  CONSTRAINT `songs_ibfk_1` FOREIGN KEY (`album_id`) REFERENCES `album` (`id`),"
    "  CONSTRAINT `songs_ibfk_2` FOREIGN KEY (`artist_id`) REFERENCES `artist` (`id`),"
    "  CONSTRAINT `songs_ibfk_3` FOREIGN KEY (`file_id`) REFERENCES `files` (`id`)"
    ") ENGINE=InnoDB")


TABLES_CREATE['playlist'] = (
    "CREATE TABLE `playlist` ("
    "  `id` int unsigned NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(100) NOT NULL,"
    "  `genre` varchar(100) DEFAULT NULL,"
    "  `song_id` int unsigned NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  KEY `song_id` (`song_id`),"
    "  CONSTRAINT `playlist_ibfk_1` FOREIGN KEY (`song_id`) REFERENCES `songs` (`id`)"
    ") ENGINE=InnoDB")


TABLES_DROP = {}

TABLES_DROP['artist'] = ()


TABLES_DROP['album'] = ()


TABLES_DROP['files'] = ()


TABLES_DROP['songs'] = ()


TABLES_DROP['playlist'] = ()

# 2021-04-18 19:34:53
