SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;

SET NAMES utf8mb4;

CREATE TABLE `Album` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `tracks` int unsigned NOT NULL,
  `year` int unsigned NOT NULL,
  `image` mediumblob,
  `artist_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `artist_id` (`artist_id`),
  CONSTRAINT `Album_ibfk_1` FOREIGN KEY (`artist_id`) REFERENCES `Artist` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Artist` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Files` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `path` varchar(512) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Playlist` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `song_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `song_id` (`song_id`),
  CONSTRAINT `Playlist_ibfk_1` FOREIGN KEY (`song_id`) REFERENCES `Songs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Songs` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `duration` float unsigned NOT NULL,
  `track` int unsigned NOT NULL,
  `file_id` int unsigned NOT NULL,
  `album_id` int unsigned NOT NULL,
  `artist_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `album_id` (`album_id`),
  KEY `artist_id` (`artist_id`),
  KEY `file_id` (`file_id`),
  CONSTRAINT `Songs_ibfk_1` FOREIGN KEY (`album_id`) REFERENCES `Album` (`id`),
  CONSTRAINT `Songs_ibfk_2` FOREIGN KEY (`artist_id`) REFERENCES `Artist` (`id`),
  CONSTRAINT `Songs_ibfk_3` FOREIGN KEY (`file_id`) REFERENCES `Files` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- 2021-04-18 19:34:53

