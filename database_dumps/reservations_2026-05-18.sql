/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.3-MariaDB, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: reservations
-- ------------------------------------------------------
-- Server version	11.8.3-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `artist_type`
--

DROP TABLE IF EXISTS `artist_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `artist_type` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `artist_id` bigint(20) NOT NULL,
  `type_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `artist_type_artist_id_149b3981_fk_artists_id` (`artist_id`),
  KEY `artist_type_type_id_ddfedbec_fk_types_id` (`type_id`),
  CONSTRAINT `artist_type_artist_id_149b3981_fk_artists_id` FOREIGN KEY (`artist_id`) REFERENCES `artists` (`id`),
  CONSTRAINT `artist_type_type_id_ddfedbec_fk_types_id` FOREIGN KEY (`type_id`) REFERENCES `types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artist_type`
--

LOCK TABLES `artist_type` WRITE;
/*!40000 ALTER TABLE `artist_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `artist_type` VALUES
(1,1,1),
(2,1,3),
(3,2,2);
/*!40000 ALTER TABLE `artist_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `artist_type_show`
--

DROP TABLE IF EXISTS `artist_type_show`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `artist_type_show` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `artist_type_id` bigint(20) NOT NULL,
  `show_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `artist_type_show_show_id_artist_type_id_b2b04eb2_uniq` (`show_id`,`artist_type_id`),
  KEY `artist_type_show_artist_type_id_a12f3364_fk_artist_type_id` (`artist_type_id`),
  CONSTRAINT `artist_type_show_artist_type_id_a12f3364_fk_artist_type_id` FOREIGN KEY (`artist_type_id`) REFERENCES `artist_type` (`id`),
  CONSTRAINT `artist_type_show_show_id_656adc7c_fk_shows_id` FOREIGN KEY (`show_id`) REFERENCES `shows` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artist_type_show`
--

LOCK TABLES `artist_type_show` WRITE;
/*!40000 ALTER TABLE `artist_type_show` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `artist_type_show` VALUES
(1,1,1),
(3,2,1),
(2,3,1);
/*!40000 ALTER TABLE `artist_type_show` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `artists`
--

DROP TABLE IF EXISTS `artists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `artists` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(60) NOT NULL,
  `lastname` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_firstname_lastname` (`firstname`,`lastname`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artists`
--

LOCK TABLES `artists` WRITE;
/*!40000 ALTER TABLE `artists` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `artists` VALUES
(5,'Anne Marie','Loop'),
(10,'Claude','Semal'),
(1,'Daniel','Marcelin'),
(8,'Élena','Perez'),
(9,'Guillaume','Alexandre'),
(13,'Gwendoline','Gauthier'),
(15,'Jaimie','Lynn'),
(11,'Laurence','Warin'),
(7,'Laurent','Caron'),
(3,'Marius','Von Mayenburg'),
(4,'Olivier','Boudon'),
(2,'Philippe','Laurent'),
(12,'Pierre','Wayburn'),
(6,'Pietro','Varasso');
/*!40000 ALTER TABLE `artists` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_group` VALUES
(1,'ADMIN'),
(2,'MEMBER');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_group_permissions` VALUES
(1,1,1),
(2,1,2),
(3,1,3),
(4,1,4),
(5,1,5),
(6,1,6),
(7,1,7),
(8,1,8),
(9,1,9),
(10,1,10),
(11,1,11),
(12,1,12),
(13,1,13),
(14,1,14),
(15,1,15),
(16,1,16),
(17,1,17),
(18,1,18),
(19,1,19),
(20,1,20),
(21,1,21),
(22,1,22),
(23,1,23),
(24,1,24),
(25,1,25),
(26,1,26),
(27,1,27),
(28,1,28),
(29,1,29),
(30,1,30),
(31,1,31),
(32,1,32),
(33,2,4);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add user',4,'add_user'),
(14,'Can change user',4,'change_user'),
(15,'Can delete user',4,'delete_user'),
(16,'Can view user',4,'view_user'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add artist',7,'add_artist'),
(26,'Can change artist',7,'change_artist'),
(27,'Can delete artist',7,'delete_artist'),
(28,'Can view artist',7,'view_artist'),
(29,'Can add user meta',8,'add_usermeta'),
(30,'Can change user meta',8,'change_usermeta'),
(31,'Can delete user meta',8,'delete_usermeta'),
(32,'Can view user meta',8,'view_usermeta'),
(33,'Can add type',9,'add_type'),
(34,'Can change type',9,'change_type'),
(35,'Can delete type',9,'delete_type'),
(36,'Can view type',9,'view_type'),
(37,'Can add locality',10,'add_locality'),
(38,'Can change locality',10,'change_locality'),
(39,'Can delete locality',10,'delete_locality'),
(40,'Can view locality',10,'view_locality'),
(41,'Can add price',11,'add_price'),
(42,'Can change price',11,'change_price'),
(43,'Can delete price',11,'delete_price'),
(44,'Can view price',11,'view_price'),
(45,'Can add location',12,'add_location'),
(46,'Can change location',12,'change_location'),
(47,'Can delete location',12,'delete_location'),
(48,'Can view location',12,'view_location'),
(49,'Can add reservation',13,'add_reservation'),
(50,'Can change reservation',13,'change_reservation'),
(51,'Can delete reservation',13,'delete_reservation'),
(52,'Can view reservation',13,'view_reservation'),
(53,'Can add show',14,'add_show'),
(54,'Can change show',14,'change_show'),
(55,'Can delete show',14,'delete_show'),
(56,'Can view show',14,'view_show'),
(57,'Can add representation',15,'add_representation'),
(58,'Can change representation',15,'change_representation'),
(59,'Can delete representation',15,'delete_representation'),
(60,'Can view representation',15,'view_representation'),
(61,'Can add review',16,'add_review'),
(62,'Can change review',16,'change_review'),
(63,'Can delete review',16,'delete_review'),
(64,'Can view review',16,'view_review'),
(65,'Can add artist type',17,'add_artisttype'),
(66,'Can change artist type',17,'change_artisttype'),
(67,'Can delete artist type',17,'delete_artisttype'),
(68,'Can view artist type',17,'view_artisttype'),
(69,'Can add artist type show',18,'add_artisttypeshow'),
(70,'Can change artist type show',18,'change_artisttypeshow'),
(71,'Can delete artist type show',18,'delete_artisttypeshow'),
(72,'Can view artist type show',18,'view_artisttypeshow'),
(73,'Can add price show',19,'add_priceshow'),
(74,'Can change price show',19,'change_priceshow'),
(75,'Can delete price show',19,'delete_priceshow'),
(76,'Can view price show',19,'view_priceshow'),
(77,'Can add representation reservation',20,'add_representationreservation'),
(78,'Can change representation reservation',20,'change_representationreservation'),
(79,'Can delete representation reservation',20,'delete_representationreservation'),
(80,'Can view representation reservation',20,'view_representationreservation');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_user` VALUES
(1,'pbkdf2_sha256$1000000$kJcSfd1Nnhw0XdEPDjaiaI$VcCA93pR3VB9kq1mxuJkAjAaAqF/60yrsHnYja9UAX8=','2025-10-23 17:31:07.814000',1,'admin','','','dimitritchamako@gmail.com',1,1,'2025-10-23 17:22:36.556000'),
(2,'pbkdf2_sha256$1000000$05Natu44mw68VcQSEVWwpT$wfWpu3R+CWe9RWrKIR6jUFOYLLHDICkBPLr7uJ/wHlQ=','2025-10-27 17:22:09.990264',0,'anna','Anna','Lyse','anna.lyse@sull.com',0,1,'2025-10-23 18:36:05.000000'),
(3,'pbkdf2_sha256$1000000$o0Hfs1tgXJi2jH9GYUEmbq$LcNYiGHZswcbuIDpwjZnNu8q9v+9bAC3Z/lkwOgTcp0=','2026-02-05 21:26:04.622126',1,'bob','Bob','Sull','bob@sull.com',1,1,'2025-10-23 18:45:31.000000'),
(4,'pbkdf2_sha256$1000000$N69SlJLkGEw00PvvkdAB3a$98cfKf3g+lkaRPqC2rMAmNtYN3LH+dxaqEnJUG3UdeM=','2025-10-28 11:44:33.304930',0,'dimi','','','',0,1,'2025-10-28 11:43:24.107146'),
(5,'pbkdf2_sha256$1000000$uZn4Igm7r0z9PVZJi7Lt9t$pcHpL75KyPRWb+uFFVx/rA6j7l/eoWViquw1Toj4dzA=',NULL,1,'dimson','','','tvd4468@gmail.com',1,1,'2026-01-06 21:28:57.558197');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_user_groups` VALUES
(1,2,2),
(2,3,1);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_user_user_permissions` VALUES
(1,3,1),
(2,3,2),
(3,3,3),
(4,3,4),
(5,3,5),
(6,3,6),
(7,3,7),
(8,3,8),
(9,3,9),
(10,3,10),
(11,3,11),
(12,3,12),
(13,3,13),
(14,3,14),
(15,3,15),
(16,3,16),
(17,3,17),
(18,3,18),
(19,3,19),
(20,3,20),
(21,3,21),
(22,3,22),
(23,3,23),
(24,3,24),
(25,3,25),
(26,3,26),
(27,3,27),
(28,3,28),
(29,3,29),
(30,3,30),
(31,3,31),
(32,3,32),
(33,3,33),
(34,3,34),
(35,3,35),
(36,3,36),
(37,3,37),
(38,3,38),
(39,3,39),
(40,3,40),
(41,3,41),
(42,3,42),
(43,3,43),
(44,3,44),
(45,3,45),
(46,3,46),
(47,3,47),
(48,3,48),
(49,3,49),
(50,3,50),
(51,3,51),
(52,3,52),
(53,3,53),
(54,3,54),
(55,3,55),
(56,3,56),
(57,3,57),
(58,3,58),
(59,3,59),
(60,3,60),
(61,3,61),
(62,3,62),
(63,3,63),
(64,3,64),
(65,3,65),
(66,3,66),
(67,3,67),
(68,3,68),
(69,3,69),
(70,3,70),
(71,3,71),
(72,3,72),
(73,3,73),
(74,3,74),
(75,3,75),
(76,3,76),
(77,3,77),
(78,3,78),
(79,3,79),
(80,3,80);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_admin_log` VALUES
(1,'2025-10-23 18:18:16.793280','1','ADMIN',1,'[{\"added\": {}}]',3,1),
(2,'2025-10-23 18:18:50.820835','2','MEMBER',1,'[{\"added\": {}}]',3,1),
(3,'2025-10-23 18:36:06.366513','2','anna',1,'[{\"added\": {}}, {\"added\": {\"name\": \"user meta\", \"object\": \" \"}}]',4,1),
(4,'2025-10-23 18:39:48.205347','2','anna',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Groups\"]}}]',4,1),
(5,'2025-10-23 18:45:32.376284','3','bob',1,'[{\"added\": {}}, {\"added\": {\"name\": \"user meta\", \"object\": \" \"}}]',4,1),
(6,'2025-10-23 18:47:22.817648','3','bob',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Staff status\", \"Superuser status\", \"Groups\", \"Last login\"]}}]',4,1),
(7,'2026-01-21 16:25:51.529543','3','bob',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,3);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_content_type` VALUES
(1,'admin','logentry'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'auth','user'),
(7,'catalogue','artist'),
(17,'catalogue','artisttype'),
(18,'catalogue','artisttypeshow'),
(10,'catalogue','locality'),
(12,'catalogue','location'),
(11,'catalogue','price'),
(19,'catalogue','priceshow'),
(15,'catalogue','representation'),
(20,'catalogue','representationreservation'),
(13,'catalogue','reservation'),
(16,'catalogue','review'),
(14,'catalogue','show'),
(9,'catalogue','type'),
(8,'catalogue','usermeta'),
(5,'contenttypes','contenttype'),
(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2025-10-21 15:11:01.035781'),
(2,'auth','0001_initial','2025-10-21 15:11:01.617920'),
(3,'admin','0001_initial','2025-10-21 15:11:01.720457'),
(4,'admin','0002_logentry_remove_auto_add','2025-10-21 15:11:01.728677'),
(5,'admin','0003_logentry_add_action_flag_choices','2025-10-21 15:11:01.734701'),
(6,'contenttypes','0002_remove_content_type_name','2025-10-21 15:11:01.813242'),
(7,'auth','0002_alter_permission_name_max_length','2025-10-21 15:11:01.859884'),
(8,'auth','0003_alter_user_email_max_length','2025-10-21 15:11:01.891129'),
(9,'auth','0004_alter_user_username_opts','2025-10-21 15:11:01.892309'),
(10,'auth','0005_alter_user_last_login_null','2025-10-21 15:11:01.939206'),
(11,'auth','0006_require_contenttypes_0002','2025-10-21 15:11:01.939206'),
(12,'auth','0007_alter_validators_add_error_messages','2025-10-21 15:11:01.939206'),
(13,'auth','0008_alter_user_username_max_length','2025-10-21 15:11:01.984385'),
(14,'auth','0009_alter_user_last_name_max_length','2025-10-21 15:11:02.018245'),
(15,'auth','0010_alter_group_name_max_length','2025-10-21 15:11:02.057139'),
(16,'auth','0011_update_proxy_permissions','2025-10-21 15:11:02.066087'),
(17,'auth','0012_alter_user_first_name_max_length','2025-10-21 15:11:02.099281'),
(19,'sessions','0001_initial','2025-10-21 15:11:02.160617'),
(20,'catalogue','0001_initial','2025-10-21 15:18:30.898243'),
(21,'catalogue','0002_usermeta','2025-10-23 18:08:22.687394'),
(22,'catalogue','0003_type','2025-11-25 09:10:43.506353'),
(23,'catalogue','0004_locality_price','2025-11-25 15:33:47.297153'),
(24,'catalogue','0005_location','2025-11-25 16:45:41.484997'),
(25,'catalogue','0006_reservation','2025-11-25 18:01:45.939600'),
(27,'catalogue','0007_show_locality_unique_postal_code_locality_and_more','2025-12-01 20:43:51.142884'),
(28,'catalogue','0008_representation','2025-12-02 12:49:05.859610'),
(29,'catalogue','0009_show_unique_slug_created_in','2025-12-02 22:10:31.093776'),
(30,'catalogue','0010_review','2025-12-02 22:26:28.998233'),
(31,'catalogue','0011_alter_review_show_alter_review_user','2025-12-02 22:35:46.490901'),
(32,'catalogue','0012_artist_types','2025-12-02 22:50:08.228023'),
(33,'catalogue','0013_remove_artist_types_artist_unique_firstname_lastname','2025-12-02 23:47:58.834792'),
(34,'catalogue','0014_artisttype','2025-12-02 23:51:58.800538'),
(35,'catalogue','0015_artisttypeshow_show_artist_types','2025-12-02 23:57:53.198396'),
(36,'catalogue','0016_priceshow_remove_show_artist_types_and_more','2025-12-03 10:13:54.764266'),
(37,'catalogue','0017_representationreservation_and_more','2025-12-03 10:24:13.917532'),
(38,'catalogue','0018_alter_reservation_status','2026-05-18 09:39:25.928838');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_session` VALUES
('3t9kvq26fux848jklln1a8p0iasl18x9','.eJxVjEsOwiAUAO_C2hA-hYJL9z0DebwHUjWQlHZlvLsh6UK3M5N5swDHXsLR0xZWYlem2eWXRcBnqkPQA-q9cWx139bIR8JP2_nSKL1uZ_s3KNDL2KYpK-OTAE9eG6eQSIAywsoINjkgI2aFeZJ5Ru0EWsxWOCNtJJAU2ecL5S84JQ:1viZhm:vP6mKpjcUvtWwbF-4THLIPBcGPwr2pDCHKg4zGOnVR0','2026-02-04 15:01:10.247761'),
('hjk61556j76y1frljp5uakcq6cvcp4ab','.eJxVjEsOwiAUAO_C2hA-hYJL9z0DebwHUjWQlHZlvLsh6UK3M5N5swDHXsLR0xZWYlem2eWXRcBnqkPQA-q9cWx139bIR8JP2_nSKL1uZ_s3KNDL2KYpK-OTAE9eG6eQSIAywsoINjkgI2aFeZJ5Ru0EWsxWOCNtJJAU2ecL5S84JQ:1vEWUR:TF4-GXUWabGLocsJ_aBDlw7gtrJ5qvwlL-3R8uCEkiY','2025-11-13 17:31:11.644458'),
('jybr4mhdsttu96w994sa2ug0y4tenebw','.eJxVjEsOwiAUAO_C2hA-hYJL9z0DebwHUjWQlHZlvLsh6UK3M5N5swDHXsLR0xZWYlem2eWXRcBnqkPQA-q9cWx139bIR8JP2_nSKL1uZ_s3KNDL2KYpK-OTAE9eG6eQSIAywsoINjkgI2aFeZJ5Ru0EWsxWOCNtJJAU2ecL5S84JQ:1vOdH8:5JVkOyA9BvdOOChQ-B2s4ttvxbfF1J3UsH3xxhxi4AA','2025-12-11 14:47:14.917054');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `localities`
--

DROP TABLE IF EXISTS `localities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `localities` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `postal_code` varchar(6) NOT NULL,
  `locality` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `localities`
--

LOCK TABLES `localities` WRITE;
/*!40000 ALTER TABLE `localities` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `localities` VALUES
(1,'1000','Bruxelles'),
(2,'1040','Etterbeek'),
(3,'1050','Ixelles'),
(4,'1170','Watermael-Boistfort'),
(5,'4000','Namur');
/*!40000 ALTER TABLE `localities` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `locations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `slug` varchar(60) NOT NULL,
  `designation` varchar(60) NOT NULL,
  `address` varchar(255) NOT NULL,
  `website` varchar(255) DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `locality_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `locations_locality_id_22dd0b44_fk_localities_id` (`locality_id`),
  CONSTRAINT `locations_locality_id_22dd0b44_fk_localities_id` FOREIGN KEY (`locality_id`) REFERENCES `localities` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locations`
--

LOCK TABLES `locations` WRITE;
/*!40000 ALTER TABLE `locations` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `locations` VALUES
(1,'art-center','Art Center','',NULL,NULL,1),
(2,'atrium','Atrium','',NULL,NULL,1),
(3,'opera-house','Opera House','',NULL,NULL,2),
(4,'espace-delvaux-la-venerie','Espace Delvaux / La Vénerie','3 rue Gratès','https://www.lavenerie.be','+32 (0)2/663.85.50',4),
(5,'dexia-art-center','Dexia Art Center','50 rue de l\'Ecuyer',NULL,NULL,1),
(6,'la-samaritaine','La Samaritaine','16 rue de la samaritaine','http://www.lasamaritaine.be/',NULL,1),
(7,'espace-magh','Espace Magh','17 rue du Poinçon','http://www.espacemagh.be','+32 (0)2/274.05.10',1);
/*!40000 ALTER TABLE `locations` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `price_show`
--

DROP TABLE IF EXISTS `price_show`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `price_show` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `price_id` bigint(20) NOT NULL,
  `show_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `price_show_show_id_price_id_8ab54424_uniq` (`show_id`,`price_id`),
  KEY `price_show_price_id_ee9e3f93_fk_prices_id` (`price_id`),
  CONSTRAINT `price_show_price_id_ee9e3f93_fk_prices_id` FOREIGN KEY (`price_id`) REFERENCES `prices` (`id`),
  CONSTRAINT `price_show_show_id_0c34fc1b_fk_shows_id` FOREIGN KEY (`show_id`) REFERENCES `shows` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `price_show`
--

LOCK TABLES `price_show` WRITE;
/*!40000 ALTER TABLE `price_show` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `price_show` VALUES
(1,1,1),
(2,2,1),
(3,2,2),
(4,4,2);
/*!40000 ALTER TABLE `price_show` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `prices`
--

DROP TABLE IF EXISTS `prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `prices` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `type` varchar(30) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_price_type` (`type`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prices`
--

LOCK TABLES `prices` WRITE;
/*!40000 ALTER TABLE `prices` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `prices` VALUES
(1,'children',5.00,'Price for children under 12.','2025-12-01','2026-12-31'),
(2,'senior',8.00,'Price for adult over 65.','2025-12-01','2026-12-31'),
(3,'article 27',0.00,'Price for people who receive assistance from the local CPAS.','2025-12-01','2026-12-31'),
(4,'VIP',15.00,'Price for special guest.','2025-12-01','2026-12-31');
/*!40000 ALTER TABLE `prices` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `representation_reservation`
--

DROP TABLE IF EXISTS `representation_reservation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `representation_reservation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `price` decimal(10,2) NOT NULL,
  `quantity` smallint(5) unsigned NOT NULL CHECK (`quantity` >= 0),
  `representation_id` bigint(20) NOT NULL,
  `reservation_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `representation_reservati_representation_id_reserv_aa62f2c0_uniq` (`representation_id`,`reservation_id`),
  KEY `representation_reser_reservation_id_4605758d_fk_reservati` (`reservation_id`),
  CONSTRAINT `representation_reser_representation_id_f2680472_fk_represent` FOREIGN KEY (`representation_id`) REFERENCES `representations` (`id`),
  CONSTRAINT `representation_reser_reservation_id_4605758d_fk_reservati` FOREIGN KEY (`reservation_id`) REFERENCES `reservations` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `representation_reservation`
--

LOCK TABLES `representation_reservation` WRITE;
/*!40000 ALTER TABLE `representation_reservation` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `representation_reservation` VALUES
(1,15.00,2,1,1);
/*!40000 ALTER TABLE `representation_reservation` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `representations`
--

DROP TABLE IF EXISTS `representations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `representations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `schedule` datetime(6) NOT NULL,
  `location_id` bigint(20) DEFAULT NULL,
  `show_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `representations_location_id_860c4ba1_fk_locations_id` (`location_id`),
  KEY `representations_show_id_90b07717_fk_shows_id` (`show_id`),
  CONSTRAINT `representations_location_id_860c4ba1_fk_locations_id` FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`),
  CONSTRAINT `representations_show_id_90b07717_fk_shows_id` FOREIGN KEY (`show_id`) REFERENCES `shows` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `representations`
--

LOCK TABLES `representations` WRITE;
/*!40000 ALTER TABLE `representations` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `representations` VALUES
(1,'2012-10-12 13:30:00.000000',4,1),
(2,'2012-10-12 20:30:00.000000',5,1),
(3,'2012-10-02 20:30:00.000000',NULL,2),
(4,'2012-10-16 20:30:00.000000',NULL,3);
/*!40000 ALTER TABLE `representations` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `reservations`
--

DROP TABLE IF EXISTS `reservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `booking_date` datetime(6) NOT NULL,
  `status` varchar(60) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reservations_user_id_d03abc5b_fk_auth_user_id` (`user_id`),
  CONSTRAINT `reservations_user_id_d03abc5b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservations`
--

LOCK TABLES `reservations` WRITE;
/*!40000 ALTER TABLE `reservations` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `reservations` VALUES
(1,'2025-11-25 18:03:32.976000','en attente',3),
(2,'2025-11-25 18:11:26.131000','en attente',3),
(3,'2025-11-25 18:11:40.272000','annulee',3),
(4,'2025-11-25 18:11:55.466000','payee',3),
(5,'2025-11-25 18:12:08.778000','payee',2),
(6,'2025-11-27 14:24:20.830000','payée',3),
(7,'2025-11-27 14:24:33.970000','en attente',2);
/*!40000 ALTER TABLE `reservations` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `review` longtext NOT NULL,
  `stars` smallint(5) unsigned NOT NULL CHECK (`stars` >= 0),
  `validated` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `show_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reviews_show_id_53c4ca85_fk_shows_id` (`show_id`),
  KEY `reviews_user_id_c23b0903_fk_auth_user_id` (`user_id`),
  CONSTRAINT `reviews_show_id_53c4ca85_fk_shows_id` FOREIGN KEY (`show_id`) REFERENCES `shows` (`id`),
  CONSTRAINT `reviews_user_id_c23b0903_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `reviews` VALUES
(1,'Excellent.',5,1,'2025-12-02 22:28:36.077000',NULL,1,3),
(2,'Pas mal.',3,0,'2025-12-02 22:29:06.963000',NULL,2,3),
(3,'Magnifique!',5,1,'2025-12-02 22:29:32.082000',NULL,1,2),
(4,'Excellent.',5,1,'2025-12-02 22:37:14.956000',NULL,1,3),
(5,'Pas mal.',3,0,'2025-12-02 22:37:26.882000',NULL,2,3),
(6,'Magnifique!',5,1,'2025-12-02 22:38:07.524000',NULL,1,2);
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `shows`
--

DROP TABLE IF EXISTS `shows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `shows` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `slug` varchar(60) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `poster_url` varchar(255) DEFAULT NULL,
  `duration` smallint(5) unsigned DEFAULT NULL CHECK (`duration` >= 0),
  `created_in` smallint(5) unsigned NOT NULL CHECK (`created_in` >= 0),
  `bookable` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `location_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  UNIQUE KEY `unique_slug_created_in` (`slug`,`created_in`),
  KEY `shows_location_id_fk` (`location_id`),
  CONSTRAINT `shows_location_id_fk` FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shows`
--

LOCK TABLES `shows` WRITE;
/*!40000 ALTER TABLE `shows` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `shows` VALUES
(1,'ayiti','Ayiti','Un homme est bloqué à l\'aéroport.\n Questionné par les douaniers, il doit alors justifier son identité, et surtout prouver qu\'il est haïtien - Qu\'est-ce qu\'être haïtien ?','ayiti.jpg',90,2010,1,'2025-01-07 17:41:03.509000',NULL,4),
(2,'cible-mouvante','Cible mouvante','Dans ce « thriller d\'anticipation », des adultes semblent alimenter et véhiculer une crainte féroce envers les enfants âgés entre 10 et 12 ans.','cible.jpg',90,2012,1,'2025-01-07 17:41:15.554000',NULL,5),
(3,'ceci-nest-pas-un-chanteur-belge','Ceci n\'est pas un chanteur belge','Non peut-être ?!\nEntre Magritte (pour le surréalisme comique) et Maigret (pour le réalisme mélancolique), ce dixième opus semalien propose quatorze nouvelles chansons mêlées à de petits textes humoristiques et à quelques fortes images poétiques.','ceci-nest-pas-un-chanteur-belge.jpg',90,2014,0,'2025-01-07 17:41:15.585000',NULL,NULL),
(4,'manneke','Manneke… !','A tour de rôle, Pierre se joue de ses oncles, tantes, grands-parents et surtout de sa mère.','manneke.jpg',90,2011,1,'2025-01-07 17:41:40.894000',NULL,6);
/*!40000 ALTER TABLE `shows` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `types`
--

DROP TABLE IF EXISTS `types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `types` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `type` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `types`
--

LOCK TABLES `types` WRITE;
/*!40000 ALTER TABLE `types` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `types` VALUES
(1,'auteur'),
(2,'scénographe'),
(3,'comédien');
/*!40000 ALTER TABLE `types` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `user_meta`
--

DROP TABLE IF EXISTS `user_meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_meta` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `langue` varchar(2) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_meta_user_id_58c29229_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_meta`
--

LOCK TABLES `user_meta` WRITE;
/*!40000 ALTER TABLE `user_meta` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `user_meta` VALUES
(1,'en',2),
(2,'fr',3);
/*!40000 ALTER TABLE `user_meta` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping routines for database 'reservations'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-05-18 20:08:26
