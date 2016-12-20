# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.5.5-10.0.21-MariaDB)
# Datenbank: parkingdata
# Erstellt am: 2016-12-02 11:55:36 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Export von Tabelle aggregateddata
# ------------------------------------------------------------

DROP TABLE IF EXISTS `aggregateddata`;

CREATE TABLE `aggregateddata` (
  `id` bigint(20) NOT NULL,
  `target` varchar(255) DEFAULT NULL,
  `target_id` bigint(45) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL COMMENT 'e.g. PARKING_SPOT, INCIDENT, etc.',
  `value` longtext COMMENT 'int value or report text',
  `datetime` datetime DEFAULT NULL,
  `geohash` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entryid` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `aggregateddata` WRITE;
/*!40000 ALTER TABLE `aggregateddata` DISABLE KEYS */;

INSERT INTO `aggregateddata` (`id`, `target`, `target_id`, `type`, `value`, `datetime`, `geohash`)
VALUES
	(0,'parklocation',1,'spots_total','20','2016-12-02 12:08:16',NULL),
	(1,'parklocation',1,'spots_free','5','2016-12-02 12:08:16',NULL),
	(2,'parklocation',1,'open','true','2016-12-02 12:08:16',NULL),
	(3,'parklocation',1,'spots_used','12','2016-12-02 12:08:16',NULL),
	(4,'praklocation',1,'spots_incident','3','2016-12-02 12:08:16',NULL),
	(5,'parkolcation',2,'spots_free','10',NULL,NULL);

/*!40000 ALTER TABLE `aggregateddata` ENABLE KEYS */;
UNLOCK TABLES;


# Export von Tabelle incomingdata
# ------------------------------------------------------------

DROP TABLE IF EXISTS `incomingdata`;

CREATE TABLE `incomingdata` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `source` int(11) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `value` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `incomingdata` WRITE;
/*!40000 ALTER TABLE `incomingdata` DISABLE KEYS */;

INSERT INTO `incomingdata` (`id`, `source`, `datetime`, `type`, `value`)
VALUES
	(1,1,'2016-12-02 11:51:43','sensor_sonah','sensor: 10\n  datetime: NOW()\n  temp: 17.34\n  battery: 87\n  gsm: 50|28\n  parkingspots:\n    1:\n      status: free\n    2:\n      status: free\n    4:\n      status: free\n    7:\n      status: blocked');

/*!40000 ALTER TABLE `incomingdata` ENABLE KEYS */;
UNLOCK TABLES;


# Export von Tabelle parkingspot
# ------------------------------------------------------------

DROP TABLE IF EXISTS `parkingspot`;

CREATE TABLE `parkingspot` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `lat` decimal(10,0) DEFAULT NULL,
  `long` decimal(10,0) DEFAULT NULL,
  `geometry` geometry DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `geohash` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `parkingspot` WRITE;
/*!40000 ALTER TABLE `parkingspot` DISABLE KEYS */;

INSERT INTO `parkingspot` (`id`, `lat`, `long`, `geometry`, `type`, `geohash`)
VALUES
	(1,100,101,NULL,'parkingspot_free',NULL),
	(2,100,99,NULL,'parkingspot_female',NULL),
	(3,100,98,NULL,'parkingspot_biking',NULL),
	(4,100,101,NULL,'parkingspot_free',NULL),
	(5,100,99,NULL,'parkingspot_female',NULL),
	(6,100,98,NULL,'parkingspot_biking',NULL),
	(7,100,101,NULL,'parkingspot_free',NULL),
	(8,100,99,NULL,'parkingspot_female',NULL),
	(9,100,98,NULL,'parkingspot_biking',NULL),
	(10,100,101,NULL,'parkingspot_free',NULL),
	(11,100,99,NULL,'parkingspot_female',NULL),
	(12,100,101,NULL,'parkingspot_free',NULL),
	(13,100,101,NULL,'parkingspot_free',NULL),
	(14,97,104,NULL,'parkingspot_blocked',NULL),
	(15,97,103,NULL,'parkingspot_private',NULL);

/*!40000 ALTER TABLE `parkingspot` ENABLE KEYS */;
UNLOCK TABLES;


# Export von Tabelle parklocation
# ------------------------------------------------------------

DROP TABLE IF EXISTS `parklocation`;

CREATE TABLE `parklocation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `lat` decimal(10,0) DEFAULT NULL,
  `long` decimal(10,0) DEFAULT NULL,
  `geohash` varchar(255) DEFAULT NULL,
  `area_geometry` geometry DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `parklocation` WRITE;
/*!40000 ALTER TABLE `parklocation` DISABLE KEYS */;

INSERT INTO `parklocation` (`id`, `name`, `lat`, `long`, `geohash`, `area_geometry`, `created_at`, `updated_at`, `deleted_at`)
VALUES
	(1,'Ededka',10,10,NULL,NULL,'2016-12-02 11:54:15','2016-12-02 11:54:15',NULL);

/*!40000 ALTER TABLE `parklocation` ENABLE KEYS */;
UNLOCK TABLES;


# Export von Tabelle parklocation_parkingspot
# ------------------------------------------------------------

DROP TABLE IF EXISTS `parklocation_parkingspot`;

CREATE TABLE `parklocation_parkingspot` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `parkingspot` bigint(45) DEFAULT NULL,
  `parklocation` bigint(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `parklocation_parkingspot` WRITE;
/*!40000 ALTER TABLE `parklocation_parkingspot` DISABLE KEYS */;

INSERT INTO `parklocation_parkingspot` (`id`, `parkingspot`, `parklocation`)
VALUES
	(1,1,1),
	(2,2,1),
	(3,3,1);

/*!40000 ALTER TABLE `parklocation_parkingspot` ENABLE KEYS */;
UNLOCK TABLES;


# Export von Tabelle source_parklocation
# ------------------------------------------------------------

DROP TABLE IF EXISTS `source_parklocation`;

CREATE TABLE `source_parklocation` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `source` int(11) DEFAULT NULL,
  `parklocation` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Export von Tabelle sources
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sources`;

CREATE TABLE `sources` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(45) DEFAULT NULL COMMENT 'e.g. SENSOR, APAG, CAMBIO, etc.',
  `location` varchar(100) DEFAULT NULL COMMENT 'Geohash',
  `owner` int(11) DEFAULT NULL,
  `lat` decimal(10,0) DEFAULT NULL,
  `long` decimal(10,0) DEFAULT NULL,
  `range_of_vision` geometry DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `sources` WRITE;
/*!40000 ALTER TABLE `sources` DISABLE KEYS */;

INSERT INTO `sources` (`id`, `type`, `location`, `owner`, `lat`, `long`, `range_of_vision`, `created_at`, `updated_at`, `deleted_at`)
VALUES
	(1,'sensor_sonah',NULL,0,100,100,NULL,'2016-12-02 11:58:32','2016-12-02 11:58:32',NULL);

/*!40000 ALTER TABLE `sources` ENABLE KEYS */;
UNLOCK TABLES;


# Export von Tabelle type
# ------------------------------------------------------------

DROP TABLE IF EXISTS `type`;

CREATE TABLE `type` (
  `idtype` int(11) NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`idtype`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
