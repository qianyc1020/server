-- MySQL dump 10.13  Distrib 8.0.16, for Linux (x86_64)
--
-- Host: localhost    Database: pygame
-- ------------------------------------------------------
-- Server version	8.0.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `nick_name` blob,
  `sex` int(11) DEFAULT '0',
  `head_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pswd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_time` int(10) unsigned DEFAULT '0',
  `last_time` int(10) unsigned DEFAULT '0',
  `last_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `account_state` int(11) DEFAULT '0',
  `gold` decimal(19,2) DEFAULT '0.00',
  `integral` decimal(19,2) DEFAULT '0.00',
  `bank_pswd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bank_gold` decimal(19,2) DEFAULT '0.00',
  `bank_integral` decimal(19,2) DEFAULT '0.00',
  `authority` int(10) unsigned DEFAULT '0',
  `total_count` int(10) unsigned DEFAULT '0',
  `introduce` varchar(1024) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level` int(11) unsigned DEFAULT '0',
  `experience` bigint(19) DEFAULT '0',
  `device` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `records` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `account_name` (`account_name`)
) ENGINE=InnoDB AUTO_INCREMENT=10001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES (10000,'pengyi',_binary 'pengyi',1,'','54292b463c3e765a42d20d4f76d38c91',1544611319,1544780348,'127.0.0.1:34279',0,0.00,0.00,NULL,0.00,0.00,0,0,NULL,NULL,0,0,NULL,NULL);
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bank`
--

DROP TABLE IF EXISTS `bank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `bank` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bank`
--

LOCK TABLES `bank` WRITE;
/*!40000 ALTER TABLE `bank` DISABLE KEYS */;
/*!40000 ALTER TABLE `bank` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bank_card`
--

DROP TABLE IF EXISTS `bank_card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `bank_card` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bank_name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `rel_name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_no` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `bank_No` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bank_card`
--

LOCK TABLES `bank_card` WRITE;
/*!40000 ALTER TABLE `bank_card` DISABLE KEYS */;
/*!40000 ALTER TABLE `bank_card` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_details`
--

DROP TABLE IF EXISTS `game_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `game_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `alloc_id` int(11) NOT NULL,
  `room_no` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `score` decimal(19,2) DEFAULT NULL,
  `service_charge` decimal(19,2) DEFAULT NULL,
  `time` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_details`
--

LOCK TABLES `game_details` WRITE;
/*!40000 ALTER TABLE `game_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `game_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gold`
--

DROP TABLE IF EXISTS `gold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `gold` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) NOT NULL,
  `source` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  `gold` decimal(19,2) NOT NULL,
  `total_gold` decimal(19,2) NOT NULL,
  `time` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `match_record`
--

DROP TABLE IF EXISTS `match_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `match_record` (
  `id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `alloc_id` int(11) NOT NULL,
  `room_no` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `game` blob,
  `players` varchar(5120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `scores` varchar(5120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `time` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `match_record`
--

LOCK TABLES `match_record` WRITE;
/*!40000 ALTER TABLE `match_record` DISABLE KEYS */;
/*!40000 ALTER TABLE `match_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_account`
--

DROP TABLE IF EXISTS `t_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_account` (
  `id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `version` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `user_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `salt` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_login_ip` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_login_date` datetime DEFAULT NULL,
  `last_login_platform` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `token` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `head` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_bra3d01udoynrrc162vsurjti` (`user_name`),
  UNIQUE KEY `UK_c1b4lrws09av75dvw3vg6uccb` (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_account`
--

LOCK TABLES `t_account` WRITE;
/*!40000 ALTER TABLE `t_account` DISABLE KEYS */;
INSERT INTO `t_account` VALUES ('402880e76729fee501672a32d5e30004',165,'2018-11-19 12:20:34','admin','1eaca8b7f7128e85aba43181801d7921','7190a55ef2346dbf5917f8ad03965666','127.0.0.1','2019-05-27 10:14:38','PC','','',1),('402880e76729fee501672a32d5e30005',9,'2018-11-19 12:20:34','user','9797fb35d4685e4f3935a70dd668c690','7190a55ef2346dbf5917f8ad03965666','0:0:0:0:0:0:0:1','2018-11-23 12:02:41','PC','1','',1);
/*!40000 ALTER TABLE `t_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_account_role`
--

DROP TABLE IF EXISTS `t_account_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_account_role` (
  `account_id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role_id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  KEY `FK_pgish3unlt9gi56tei7isfs28` (`role_id`),
  KEY `FK_s3hs3kjeite8e9hqxl21v2pix` (`account_id`),
  CONSTRAINT `FK_pgish3unlt9gi56tei7isfs28` FOREIGN KEY (`role_id`) REFERENCES `t_role` (`id`),
  CONSTRAINT `FK_s3hs3kjeite8e9hqxl21v2pix` FOREIGN KEY (`account_id`) REFERENCES `t_account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_account_role`
--

LOCK TABLES `t_account_role` WRITE;
/*!40000 ALTER TABLE `t_account_role` DISABLE KEYS */;
INSERT INTO `t_account_role` VALUES ('402880e76729fee501672a32d5e30005','402880e76729fee501672a30766a0000'),('402880e76729fee501672a32d5e30004','402880e76729fee501672a3673580008');
/*!40000 ALTER TABLE `t_account_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_gamerecord`
--

DROP TABLE IF EXISTS `t_gamerecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_gamerecord` (
  `id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `version` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `user_names` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `game_info` varchar(10000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `base_score` int(11) DEFAULT NULL,
  `game_type` int(11) DEFAULT NULL,
  `room_owner` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `total_round` int(11) DEFAULT NULL,
  `room_no` int(11) DEFAULT NULL,
  `rule` int(11) DEFAULT NULL,
  `double_bull` bit(1) DEFAULT NULL,
  `spotted_bull` bit(1) DEFAULT NULL,
  `bomb_bull` bit(1) DEFAULT NULL,
  `small_bull` bit(1) DEFAULT NULL,
  `player_push` bit(1) DEFAULT NULL,
  `started_into` bit(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_gamerecord`
--

LOCK TABLES `t_gamerecord` WRITE;
/*!40000 ALTER TABLE `t_gamerecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_gamerecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_gold_detailed`
--

DROP TABLE IF EXISTS `t_gold_detailed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_gold_detailed` (
  `id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `version` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `user_id` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gold` decimal(19,2) DEFAULT NULL,
  `flow_type` int(11) DEFAULT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `old_gold` decimal(19,2) DEFAULT NULL,
  `new_gold` decimal(19,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_23g3265xxetdoqch6otet7fpt` (`user_id`),
  CONSTRAINT `FK_23g3265xxetdoqch6otet7fpt` FOREIGN KEY (`user_id`) REFERENCES `t_user` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_gold_detailed`
--

LOCK TABLES `t_gold_detailed` WRITE;
/*!40000 ALTER TABLE `t_gold_detailed` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_gold_detailed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_logger`
--

DROP TABLE IF EXISTS `t_logger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_logger` (
  `id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `version` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `operation_user` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `logger_type` int(11) DEFAULT NULL,
  `logger_content` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ip` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_qgoksk3v1unfsqypj5dog67wq` (`operation_user`),
  CONSTRAINT `FK_qgoksk3v1unfsqypj5dog67wq` FOREIGN KEY (`operation_user`) REFERENCES `t_user` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_logger`
--

LOCK TABLES `t_logger` WRITE;
/*!40000 ALTER TABLE `t_logger` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_logger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_money_detailed`
--

DROP TABLE IF EXISTS `t_money_detailed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_money_detailed` (
  `id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `version` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `user_id` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `money` decimal(19,2) DEFAULT NULL,
  `flow_type` int(11) DEFAULT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `old_money` decimal(19,2) DEFAULT NULL,
  `new_money` decimal(19,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_q2nmffbjynsjh5k4u0f68ffo3` (`user_id`),
  CONSTRAINT `FK_q2nmffbjynsjh5k4u0f68ffo3` FOREIGN KEY (`user_id`) REFERENCES `t_user` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_money_detailed`
--

LOCK TABLES `t_money_detailed` WRITE;
/*!40000 ALTER TABLE `t_money_detailed` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_money_detailed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_notice`
--

DROP TABLE IF EXISTS `t_notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_notice` (
  `id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `version` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `content` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_notice`
--

LOCK TABLES `t_notice` WRITE;
/*!40000 ALTER TABLE `t_notice` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_notice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_permission`
--

DROP TABLE IF EXISTS `t_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_permission` (
  `id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `version` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `value` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_permission`
--

LOCK TABLES `t_permission` WRITE;
/*!40000 ALTER TABLE `t_permission` DISABLE KEYS */;
INSERT INTO `t_permission` VALUES ('402880e76729fee501672a3606350006',5,'2018-11-19 12:24:03','/system/edit','系统配置修改','/system/*',1),('402880e767309aa1016730abd3230005',1,'2018-11-20 18:30:26','/recharge_give/pagination','赠送','/recharge_give/*',1),('402880e76733ef6f0167342a095d0002',1,'2018-11-21 10:47:09','/gamerecord/pagination','游戏记录','/gamerecord/*',1);
/*!40000 ALTER TABLE `t_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_recharge`
--

DROP TABLE IF EXISTS `t_recharge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_recharge` (
  `id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `version` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `recharge_no` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `money` decimal(19,2) DEFAULT NULL,
  `pay_time` datetime DEFAULT NULL,
  `pay_type` int(11) DEFAULT NULL,
  `is_success` int(11) DEFAULT NULL,
  `select_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notify_time` datetime DEFAULT NULL,
  `before_card` int(11) DEFAULT NULL,
  `before_gold` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_recharge_give`
--

DROP TABLE IF EXISTS `t_recharge_give`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_recharge_give` (
  `id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `version` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `money` decimal(19,2) DEFAULT NULL,
  `give_money` decimal(19,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_recharge_give`
--

LOCK TABLES `t_recharge_give` WRITE;
/*!40000 ALTER TABLE `t_recharge_give` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_recharge_give` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_recharge_select`
--

DROP TABLE IF EXISTS `t_recharge_select`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_recharge_select` (
  `id` tinytext COLLATE utf8mb4_unicode_ci,
  `version` int(11) DEFAULT NULL,
  `create_date` timestamp NULL DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `price` decimal(19,2) DEFAULT NULL,
  `give_currency` int(11) DEFAULT NULL,
  `currency` int(11) DEFAULT NULL,
  `agent` bit(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_recharge_select`
--

LOCK TABLES `t_recharge_select` WRITE;
/*!40000 ALTER TABLE `t_recharge_select` DISABLE KEYS */;
INSERT INTO `t_recharge_select` VALUES ('1',0,NULL,1,100.00,0,1,_binary ''),('2',0,NULL,1,500.00,0,50000,_binary ''),('1',0,NULL,1,1.00,0,1,_binary '');
/*!40000 ALTER TABLE `t_recharge_select` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_role`
--

DROP TABLE IF EXISTS `t_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_role` (
  `id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `version` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_role`
--

LOCK TABLES `t_role` WRITE;
/*!40000 ALTER TABLE `t_role` DISABLE KEYS */;
INSERT INTO `t_role` VALUES ('402880e76729fee501672a30766a0000',8,'2018-11-19 12:17:58','总后台','用户总后台',1),('402880e76729fee501672a3673580008',3,'2018-11-19 12:24:31','admin','超级管理',1);
/*!40000 ALTER TABLE `t_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_role_permission`
--

DROP TABLE IF EXISTS `t_role_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_role_permission` (
  `role_id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `permission_id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  KEY `FK_nkhhl7rlqqsu5goufwn1udr0e` (`permission_id`),
  KEY `FK_n0gk0jwxlfbi5vbmf43r0kcwl` (`role_id`),
  CONSTRAINT `FK_n0gk0jwxlfbi5vbmf43r0kcwl` FOREIGN KEY (`role_id`) REFERENCES `t_role` (`id`),
  CONSTRAINT `FK_nkhhl7rlqqsu5goufwn1udr0e` FOREIGN KEY (`permission_id`) REFERENCES `t_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_role_permission`
--

LOCK TABLES `t_role_permission` WRITE;
/*!40000 ALTER TABLE `t_role_permission` DISABLE KEYS */;
INSERT INTO `t_role_permission` VALUES ('402880e76729fee501672a30766a0000','402880e76729fee501672a3606350006'),('402880e76729fee501672a3673580008','402880e76729fee501672a3606350006'),('402880e76729fee501672a3673580008','402880e76733ef6f0167342a095d0002'),('402880e76729fee501672a3673580008','402880e767309aa1016730abd3230005');
/*!40000 ALTER TABLE `t_role_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_seal`
--

DROP TABLE IF EXISTS `t_seal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_seal` (
  `id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `version` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `seal_no` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_seal`
--

LOCK TABLES `t_seal` WRITE;
/*!40000 ALTER TABLE `t_seal` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_seal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_sequence`
--

DROP TABLE IF EXISTS `t_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_sequence` (
  `id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `no` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_sequence`
--

LOCK TABLES `t_sequence` WRITE;
/*!40000 ALTER TABLE `t_sequence` DISABLE KEYS */;
INSERT INTO `t_sequence` VALUES ('2c9230cd6af88901016af88910130000',1);
/*!40000 ALTER TABLE `t_sequence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_system`
--

DROP TABLE IF EXISTS `t_system`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_system` (
  `id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `version` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `user_agreement` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ratio` decimal(19,2) DEFAULT NULL,
  `count_multiple` int(11) DEFAULT NULL,
  `register_give` decimal(19,2) DEFAULT NULL,
  `spread_give` decimal(19,2) DEFAULT NULL,
  `extension` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `payurl` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `agent_group` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `weChat_number` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `customer_service` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `share_give` int(11) DEFAULT NULL,
  `recharge_ratio` decimal(19,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_system`
--

LOCK TABLES `t_system` WRITE;
/*!40000 ALTER TABLE `t_system` DISABLE KEYS */;
INSERT INTO `t_system` VALUES ('1',1,'2018-11-19 12:19:21','0.00',0.00,0,NULL,0.00,'0','0','1',NULL,NULL,0,1.00);
/*!40000 ALTER TABLE `t_system` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_user`
--

DROP TABLE IF EXISTS `t_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_user` (
  `account_id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `parent_id` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `money` decimal(19,2) DEFAULT NULL,
  `is_vip` bit(1) DEFAULT NULL,
  `sex` int(11) DEFAULT NULL,
  `device_no` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone_no` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ranking` int(11) DEFAULT NULL,
  `spread_can_get` decimal(19,2) DEFAULT NULL,
  `spread_getted` decimal(19,2) DEFAULT NULL,
  `invite_code` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `weChat_no` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gold` decimal(19,2) DEFAULT NULL,
  `days` int(11) DEFAULT NULL,
  `reward` int(11) DEFAULT NULL,
  `benefit` int(11) DEFAULT NULL,
  PRIMARY KEY (`account_id`),
  UNIQUE KEY `UK_rux5nbedaa03mh0taouvjay7l` (`invite_code`),
  KEY `FK_qwyjcr79ow2inxsrcx4na2ngt` (`parent_id`),
  CONSTRAINT `FK_7llhaf2khhyesjrcbk4f4rmfc` FOREIGN KEY (`account_id`) REFERENCES `t_account` (`id`),
  CONSTRAINT `FK_qwyjcr79ow2inxsrcx4na2ngt` FOREIGN KEY (`parent_id`) REFERENCES `t_user` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_user`
--

LOCK TABLES `t_user` WRITE;
/*!40000 ALTER TABLE `t_user` DISABLE KEYS */;
INSERT INTO `t_user` VALUES ('402880e76729fee501672a32d5e30004',NULL,'admin',0.00,_binary '',1,NULL,NULL,10000,0.00,0.00,NULL,NULL,10000.00,NULL,NULL,NULL),('402880e76729fee501672a32d5e30005',NULL,'user',1.00,_binary '\0',1,NULL,NULL,10000,0.00,0.00,NULL,NULL,10000.00,NULL,NULL,NULL);
/*!40000 ALTER TABLE `t_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_bankcard`
--

DROP TABLE IF EXISTS `user_bankcard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user_bankcard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `bank_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bank_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone_num` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_card_num` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_bankcard`
--

LOCK TABLES `user_bankcard` WRITE;
/*!40000 ALTER TABLE `user_bankcard` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_bankcard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_phone_number`
--

DROP TABLE IF EXISTS `user_phone_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user_phone_number` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `user_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone_num` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_phone_number`
--

LOCK TABLES `user_phone_number` WRITE;
/*!40000 ALTER TABLE `user_phone_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_phone_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_withdrawal`
--

DROP TABLE IF EXISTS `user_withdrawal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user_withdrawal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_date` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `money` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pay_ment` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_drgaqg9erfd6yv5aexf7ie86o` (`user_id`),
  CONSTRAINT `FK_drgaqg9erfd6yv5aexf7ie86o` FOREIGN KEY (`user_id`) REFERENCES `account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_withdrawal`
--

LOCK TABLES `user_withdrawal` WRITE;
/*!40000 ALTER TABLE `user_withdrawal` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_withdrawal` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-04  1:08:06
