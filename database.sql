-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: bank_management
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `account_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `account_number` varchar(20) NOT NULL,
  `account_type` varchar(20) NOT NULL,
  `balance` decimal(12,2) DEFAULT '0.00',
  `status` varchar(20) DEFAULT 'Active',
  `created_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`account_id`),
  UNIQUE KEY `account_number` (`account_number`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `accounts_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (1,1,'1000001','Savings',3000.00,'Active','2026-08-09 12:05:42'),(2,2,'1000002','Savings',33000.00,'Active','2026-08-09 12:41:34'),(3,3,'1000003','Savings',50000.00,'Active','2026-08-09 12:42:42'),(4,4,'1000004','Savings',40000.00,'Active','2026-08-09 12:43:37'),(5,5,'1000005','Savings',2000.00,'Active','2026-08-09 12:45:23'),(6,6,'1000006','Savings',1000.00,'Active','2026-08-09 13:50:00');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Anitha','9876543210','anitha@gmail.com','Tiruvuru','2005-05-10'),(2,'Ravi','9876543211','ravi@gmail.com','vijayawada','2004-06-15'),(3,'Bhannu','1287543976','bhannu@gmail.com','vijayawada','2006-07-12'),(4,'Abhi sri','7895694563','abhi@gmail.com','elluru','2004-11-29'),(5,'Chinnu','2355454542','chinnu@gmail.com','hyd','2006-01-05'),(6,'Ravi Kumar','9876543211','ravi@gmail.com','Vijayawada','2004-06-15');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `account_number` varchar(20) NOT NULL,
  `transaction_type` varchar(20) NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `transaction_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `balance_after` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,'1000001','Deposit',5000.00,'2026-08-09 12:05:42',5000.00),(2,'1000001','Deposit',2000.00,'2026-08-09 12:29:58',7000.00),(3,'1000001','Withdrawal',1500.00,'2026-08-09 12:35:08',5500.00),(4,'1000002','Deposit',30000.00,'2026-08-09 12:41:34',30000.00),(5,'1000003','Deposit',50000.00,'2026-08-09 12:42:42',50000.00),(6,'1000004','Deposit',40000.00,'2026-08-09 12:43:37',40000.00),(7,'1000005','Deposit',2000.00,'2026-08-09 12:45:23',2000.00),(8,'1000001','Transfer Sent',1000.00,'2026-08-09 12:48:03',4500.00),(9,'1000002','Transfer Received',1000.00,'2026-08-09 12:48:03',31000.00),(10,'1000001','Transfer Sent',1000.00,'2026-08-09 12:54:05',3500.00),(11,'1000002','Transfer Received',1000.00,'2026-08-09 12:54:05',32000.00),(12,'1000006','Deposit',1000.00,'2026-08-09 13:50:00',1000.00),(13,'1000001','Deposit',500.00,'2026-08-09 13:56:29',4000.00),(14,'1000001','Withdrawal',500.00,'2026-08-09 14:07:50',3500.00),(15,'1000001','Transfer Sent',500.00,'2026-08-09 22:13:06',3000.00),(16,'1000002','Transfer Received',500.00,'2026-08-09 22:13:06',32500.00),(17,'1000001','Deposit',1000.00,'2026-08-10 06:18:03',4000.00),(18,'1000001','Withdrawal',500.00,'2026-08-10 06:18:28',3500.00),(19,'1000001','Transfer Sent',500.00,'2026-08-10 06:19:01',3000.00),(20,'1000002','Transfer Received',500.00,'2026-08-10 06:19:01',33000.00);
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-10  6:35:17
