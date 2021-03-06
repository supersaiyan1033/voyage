-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: voyage
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
CREATE DATABASE voyage;
USE voyage;

--
-- Table structure for table `bus`
--

DROP TABLE IF EXISTS `bus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bus` (
  `Bus_ID` int NOT NULL,
  `Company` varchar(45) NOT NULL,
  `Bus_name` varchar(45) NOT NULL,
  `seat_Capacity` int NOT NULL,
  PRIMARY KEY (`Bus_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bus`
--

LOCK TABLES `bus` WRITE;
/*!40000 ALTER TABLE `bus` DISABLE KEYS */;
INSERT INTO `bus` VALUES (1,'Voyage','b1',100),(2,'Voyage','b2',80),(3,'Voyage','b3',55),(4,'Voyage','b4',70),(5,'Voyage','b5',45);
/*!40000 ALTER TABLE `bus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bus_details`
--

DROP TABLE IF EXISTS `bus_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bus_details` (
  `Bus_ID` int NOT NULL,
  `Time_From` time NOT NULL,
  `Time_To` time NOT NULL,
  `Price` int NOT NULL,
  `Bus_No` int NOT NULL,
  `RID` int NOT NULL,
  PRIMARY KEY (`Bus_No`),
  KEY `Bus_ID_idx` (`Bus_ID`),
  KEY `RID_idx` (`RID`),
  CONSTRAINT `Bus_ID` FOREIGN KEY (`Bus_ID`) REFERENCES `bus` (`Bus_ID`),
  CONSTRAINT `RID` FOREIGN KEY (`RID`) REFERENCES `route` (`RID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bus_details`
--

LOCK TABLES `bus_details` WRITE;
/*!40000 ALTER TABLE `bus_details` DISABLE KEYS */;
INSERT INTO `bus_details` VALUES (1,'14:15:00','15:00:00',300,20,9),(2,'18:30:00','19:20:00',400,21,10),(3,'07:20:00','09:30:00',145,22,11),(1,'09:45:00','10:40:00',250,23,10),(1,'09:45:00','12:30:00',650,24,12),(5,'07:20:00','12:30:00',350,25,13),(4,'13:20:00','14:00:00',200,26,14),(4,'14:00:00','15:20:00',250,27,14),(3,'15:20:00','16:10:00',100,28,15),(3,'13:20:00','15:20:00',175,29,9),(2,'14:00:00','16:10:00',400,30,11);
/*!40000 ALTER TABLE `bus_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bus_passenger`
--

DROP TABLE IF EXISTS `bus_passenger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bus_passenger` (
  `Name` varchar(45) NOT NULL,
  `Gender` varchar(45) NOT NULL,
  `Age` int NOT NULL,
  `Booking_ID` int NOT NULL,
  `Passenger_ID` int NOT NULL AUTO_INCREMENT,
  `Seat_no` int NOT NULL,
  PRIMARY KEY (`Passenger_ID`),
  KEY `B_b_idx` (`Booking_ID`),
  CONSTRAINT `B_b` FOREIGN KEY (`Booking_ID`) REFERENCES `bus_ticket` (`Booking_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bus_passenger`
--

LOCK TABLES `bus_passenger` WRITE;
/*!40000 ALTER TABLE `bus_passenger` DISABLE KEYS */;
/*!40000 ALTER TABLE `bus_passenger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bus_schedule`
--

DROP TABLE IF EXISTS `bus_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bus_schedule` (
  `Bus_No` int NOT NULL,
  `date_from` date NOT NULL,
  `date_to` date NOT NULL,
  `no_of_seats_vacant` int DEFAULT NULL,
  `BSID` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`BSID`),
  KEY `Buses_No_idx` (`Bus_No`),
  CONSTRAINT `Buses_No` FOREIGN KEY (`Bus_No`) REFERENCES `bus_details` (`Bus_No`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bus_schedule`
--

LOCK TABLES `bus_schedule` WRITE;
/*!40000 ALTER TABLE `bus_schedule` DISABLE KEYS */;
INSERT INTO `bus_schedule` VALUES (20,'2020-11-15','2020-11-15',100,1),(21,'2020-11-15','2020-11-15',80,2),(22,'2020-11-15','2020-11-15',55,3),(23,'2020-11-15','2020-11-15',100,4),(24,'2020-11-15','2020-11-15',100,5),(25,'2020-11-15','2020-11-15',45,6),(26,'2020-11-15','2020-11-15',60,7),(27,'2020-11-15','2020-11-15',50,8),(28,'2020-11-15','2020-11-15',45,9),(29,'2020-11-15','2020-11-15',55,10),(30,'2020-11-15','2020-11-15',70,11),(25,'2020-11-16','2020-11-16',45,12),(20,'2020-11-18','2020-11-18',100,13),(20,'2020-11-19','2020-11-19',100,14),(21,'2020-11-18','2020-11-18',80,15);
/*!40000 ALTER TABLE `bus_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bus_ticket`
--

DROP TABLE IF EXISTS `bus_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bus_ticket` (
  `Booking_ID` int NOT NULL AUTO_INCREMENT,
  `User_ID` int NOT NULL,
  `Date_of_booking` datetime NOT NULL,
  `BSID` int NOT NULL,
  `No_of_passengers` int NOT NULL,
  `status` varchar(45) NOT NULL DEFAULT 'Pending',
  `amount` int NOT NULL,
  PRIMARY KEY (`Booking_ID`),
  KEY `user_b_idx` (`User_ID`),
  KEY `Bs_b_idx` (`BSID`),
  CONSTRAINT `Bs_b` FOREIGN KEY (`BSID`) REFERENCES `bus_schedule` (`BSID`),
  CONSTRAINT `user_b` FOREIGN KEY (`User_ID`) REFERENCES `users` (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bus_ticket`
--

LOCK TABLES `bus_ticket` WRITE;
/*!40000 ALTER TABLE `bus_ticket` DISABLE KEYS */;
/*!40000 ALTER TABLE `bus_ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bus_transaction`
--

DROP TABLE IF EXISTS `bus_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bus_transaction` (
  `Transaction_ID` int NOT NULL AUTO_INCREMENT,
  `booking_ID` int NOT NULL,
  `description` varchar(45) NOT NULL,
  `amount` int NOT NULL,
  PRIMARY KEY (`Transaction_ID`),
  KEY `bus_bus_idx` (`booking_ID`),
  CONSTRAINT `bus_bus` FOREIGN KEY (`booking_ID`) REFERENCES `bus_ticket` (`Booking_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bus_transaction`
--

LOCK TABLES `bus_transaction` WRITE;
/*!40000 ALTER TABLE `bus_transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `bus_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-10-06 16:46:40.076808'),(2,'auth','0001_initial','2020-10-06 16:46:40.556418'),(3,'admin','0001_initial','2020-10-06 16:46:42.027610'),(4,'admin','0002_logentry_remove_auto_add','2020-10-06 16:46:42.470446'),(5,'admin','0003_logentry_add_action_flag_choices','2020-10-06 16:46:42.485498'),(6,'contenttypes','0002_remove_content_type_name','2020-10-06 16:46:42.777998'),(7,'auth','0002_alter_permission_name_max_length','2020-10-06 16:46:43.037515'),(8,'auth','0003_alter_user_email_max_length','2020-10-06 16:46:43.121637'),(9,'auth','0004_alter_user_username_opts','2020-10-06 16:46:43.140241'),(10,'auth','0005_alter_user_last_login_null','2020-10-06 16:46:43.300531'),(11,'auth','0006_require_contenttypes_0002','2020-10-06 16:46:43.315976'),(12,'auth','0007_alter_validators_add_error_messages','2020-10-06 16:46:43.323062'),(13,'auth','0008_alter_user_username_max_length','2020-10-06 16:46:43.557727'),(14,'auth','0009_alter_user_last_name_max_length','2020-10-06 16:46:43.752379'),(15,'auth','0010_alter_group_name_max_length','2020-10-06 16:46:43.798819'),(16,'auth','0011_update_proxy_permissions','2020-10-06 16:46:43.818794'),(17,'auth','0012_alter_user_first_name_max_length','2020-10-06 16:46:44.127528'),(18,'sessions','0001_initial','2020-10-06 16:46:44.242393');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('b77vgkyoujenpeqonl85prf5w030nst8','eyJ1c2VySWQiOjE0LCJlbWFpbCI6Im5pdGluLm1ha3VsYUBnbWFpbC5jb20iLCJyb2xlIjoiYWRtaW4ifQ:1keg6a:gmHGM6j0VwF-b1wqTUzSvPEalUIDBwIF7w49_Jl5hSY','2020-11-16 15:49:24.480654');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flight`
--

DROP TABLE IF EXISTS `flight`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight` (
  `Flight_ID` int NOT NULL,
  `Company` varchar(45) NOT NULL,
  `Flight_name` varchar(45) NOT NULL,
  `seat_Capacity` int NOT NULL,
  PRIMARY KEY (`Flight_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight`
--

LOCK TABLES `flight` WRITE;
/*!40000 ALTER TABLE `flight` DISABLE KEYS */;
INSERT INTO `flight` VALUES (1,'Voyage','s1',200),(2,'Voyage','a1',300),(3,'Voyage','a2',500),(4,'Voyage','t1',100),(5,'Voyage','i1',600),(6,'Voyage','i2',250),(7,'Voyage','a3',200),(8,'Voyage','t2',450);
/*!40000 ALTER TABLE `flight` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flight_details`
--

DROP TABLE IF EXISTS `flight_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight_details` (
  `Flight_ID` int NOT NULL,
  `Time_From` time NOT NULL,
  `Time_To` time NOT NULL,
  `Price` int NOT NULL,
  `Flight_No` int NOT NULL,
  `RID` int NOT NULL,
  PRIMARY KEY (`Flight_No`),
  KEY `Flight_ID_idx` (`Flight_ID`),
  KEY `route_idx` (`RID`),
  CONSTRAINT `Flight_No` FOREIGN KEY (`Flight_ID`) REFERENCES `flight` (`Flight_ID`),
  CONSTRAINT `route` FOREIGN KEY (`RID`) REFERENCES `route` (`RID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight_details`
--

LOCK TABLES `flight_details` WRITE;
/*!40000 ALTER TABLE `flight_details` DISABLE KEYS */;
INSERT INTO `flight_details` VALUES (4,'14:15:00','15:00:00',2499,1,3),(1,'18:30:00','19:20:00',3499,2,1),(3,'07:20:00','09:30:00',3999,3,1),(3,'09:45:00','10:40:00',2899,4,3),(3,'09:45:00','12:30:00',3999,5,4),(3,'07:20:00','12:30:00',6999,6,2),(5,'13:20:00','14:00:00',2299,7,5),(5,'14:00:00','15:20:00',3299,8,1),(5,'15:20:00','16:10:00',2699,9,3),(5,'13:20:00','15:20:00',4299,10,6),(5,'13:20:00','16:10:00',7199,11,7),(5,'14:00:00','16:10:00',4299,12,8);
/*!40000 ALTER TABLE `flight_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flight_passenger`
--

DROP TABLE IF EXISTS `flight_passenger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight_passenger` (
  `Name` varchar(45) NOT NULL,
  `Gender` varchar(45) NOT NULL,
  `Age` int NOT NULL,
  `Booking_ID` int NOT NULL,
  `Passenger_ID` int NOT NULL AUTO_INCREMENT,
  `Seat_no` int NOT NULL,
  PRIMARY KEY (`Passenger_ID`),
  KEY `Booking_Id_idx` (`Booking_ID`),
  CONSTRAINT `Booking_Id` FOREIGN KEY (`Booking_ID`) REFERENCES `flight_ticket` (`Booking_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight_passenger`
--

LOCK TABLES `flight_passenger` WRITE;
/*!40000 ALTER TABLE `flight_passenger` DISABLE KEYS */;
/*!40000 ALTER TABLE `flight_passenger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flight_schedule`
--

DROP TABLE IF EXISTS `flight_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight_schedule` (
  `Flight_No` int NOT NULL,
  `date_from` date NOT NULL,
  `date_to` date NOT NULL,
  `no_of_seats_vacant` int DEFAULT NULL,
  `FSID` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`FSID`),
  KEY `ID_idx` (`no_of_seats_vacant`),
  KEY `KID_idx` (`Flight_No`),
  CONSTRAINT `F_No` FOREIGN KEY (`Flight_No`) REFERENCES `flight_details` (`Flight_No`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight_schedule`
--

LOCK TABLES `flight_schedule` WRITE;
/*!40000 ALTER TABLE `flight_schedule` DISABLE KEYS */;
INSERT INTO `flight_schedule` VALUES (1,'2020-11-15','2020-11-15',100,1),(2,'2020-11-15','2020-11-15',200,2),(3,'2020-11-15','2020-11-15',150,3),(4,'2020-11-15','2020-11-15',200,4),(5,'2020-11-15','2020-11-15',100,5),(6,'2020-11-15','2020-11-15',50,6),(7,'2020-11-15','2020-11-15',150,7),(8,'2020-11-15','2020-11-15',100,8),(9,'2020-11-15','2020-11-15',100,9),(10,'2020-11-15','2020-11-15',150,10),(11,'2020-11-15','2020-11-15',50,11),(12,'2020-11-15','2020-11-15',50,12),(2,'2020-11-18','2020-11-18',200,15),(2,'2020-11-19','2020-11-19',200,16),(2,'2020-11-16','2020-11-16',200,17),(3,'2020-11-18','2020-11-18',500,18),(4,'2020-11-18','2020-11-18',500,19),(9,'2020-11-18','2020-11-18',600,20);
/*!40000 ALTER TABLE `flight_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flight_ticket`
--

DROP TABLE IF EXISTS `flight_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight_ticket` (
  `Booking_ID` int NOT NULL AUTO_INCREMENT,
  `User_ID` int NOT NULL,
  `Date_of_booking` datetime NOT NULL,
  `FSID` int NOT NULL,
  `No_of_passengers` int NOT NULL,
  `status` varchar(45) NOT NULL DEFAULT 'Pending',
  `amount` int NOT NULL,
  PRIMARY KEY (`Booking_ID`),
  KEY `User_ID_idx` (`User_ID`),
  KEY `FSID_idx` (`FSID`),
  CONSTRAINT `FSID` FOREIGN KEY (`FSID`) REFERENCES `flight_schedule` (`FSID`),
  CONSTRAINT `User_ID` FOREIGN KEY (`User_ID`) REFERENCES `users` (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight_ticket`
--

LOCK TABLES `flight_ticket` WRITE;
/*!40000 ALTER TABLE `flight_ticket` DISABLE KEYS */;
/*!40000 ALTER TABLE `flight_ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flight_transaction`
--

DROP TABLE IF EXISTS `flight_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight_transaction` (
  `Transaction_ID` int NOT NULL AUTO_INCREMENT,
  `booking_ID` int NOT NULL,
  `description` varchar(45) NOT NULL,
  `amount` int NOT NULL,
  PRIMARY KEY (`Transaction_ID`),
  KEY `booking_ID_idx` (`booking_ID`),
  CONSTRAINT `bookings_ID` FOREIGN KEY (`booking_ID`) REFERENCES `flight_ticket` (`Booking_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight_transaction`
--

LOCK TABLES `flight_transaction` WRITE;
/*!40000 ALTER TABLE `flight_transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `flight_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `route`
--

DROP TABLE IF EXISTS `route`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `route` (
  `RID` int NOT NULL AUTO_INCREMENT,
  `from_p` varchar(45) DEFAULT NULL,
  `to_p` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`RID`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `route`
--

LOCK TABLES `route` WRITE;
/*!40000 ALTER TABLE `route` DISABLE KEYS */;
INSERT INTO `route` VALUES (1,'Chennai','Hyderabad'),(2,'Chennai','Indore'),(3,'Hyderabad','Vijayawada'),(4,'Hyderabad','Indore'),(5,'Bangalore','Chennai'),(6,'Bangalore ','Hyderabad'),(7,'Bangalore ','Vijayawada'),(8,'Chennai','Vijayawada'),(9,'Gwalior','Indore'),(10,'Jhansi','Bhopal'),(11,'Indore','Bhopal'),(12,'Gwalior','Jhansi'),(13,'Bhopal','Gwalior'),(14,'Jhansi ','Indore'),(15,'Indore','Gwalior');
/*!40000 ALTER TABLE `route` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `firstname` varchar(100) NOT NULL,
  `lastname` varchar(100) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `address` varchar(200) NOT NULL,
  `mobileno` varchar(10) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `userID` int NOT NULL AUTO_INCREMENT,
  `DOB` date NOT NULL,
  `wallet` int NOT NULL DEFAULT '100000',
  `Role` varchar(45) DEFAULT 'user',
  PRIMARY KEY (`userID`),
  UNIQUE KEY `userID_UNIQUE` (`userID`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('Nitin','Makula','Male','street no 4 plot no 128 pentareddy colony hno 3-92-31/1','9014046288','nitin.makula@gmail.com','$2b$12$CzSRs6noajZwDgRRh7JHzO/7u.Q9G1wSMcf.aVnmXa1XLhOQJ/loa',14,'2002-07-20',100000,'admin'),('Nitin','Makula','Male','street no 4 plot no 128 pentareddy colony hno 3-92-31/1','9014046288','cse190001033@iiti.ac.in','$2b$12$Z521VTEIEymRI/2pZ6r0Eu6uxfD8m5TyjMi/PBRJK.VW5oXtRs1n.',15,'2002-07-20',100000,'user');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-16 21:10:02
