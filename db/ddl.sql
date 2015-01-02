-- MySQL dump 10.14  Distrib 5.5.39-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: asprom
-- ------------------------------------------------------
-- Server version	5.5.39-MariaDB-2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `changelog`
--

DROP TABLE IF EXISTS `changelog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `changelog` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `serviceId` int(10) unsigned NOT NULL,
  `neat` tinyint(1) unsigned NOT NULL,
  `justification` varchar(500) COLLATE utf8_roman_ci DEFAULT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`,`serviceId`),
  KEY `FK__servicesa` (`serviceId`),
  CONSTRAINT `FK__servicesa` FOREIGN KEY (`serviceId`) REFERENCES `services` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_roman_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `closed`
--

DROP TABLE IF EXISTS `closed`;
/*!50001 DROP VIEW IF EXISTS `closed`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `closed` (
  `id` tinyint NOT NULL,
  `hostname` tinyint NOT NULL,
  `ip` tinyint NOT NULL,
  `port` tinyint NOT NULL,
  `product` tinyint NOT NULL,
  `version` tinyint NOT NULL,
  `extrainfo` tinyint NOT NULL,
  `justification` tinyint NOT NULL,
  `lsdate` tinyint NOT NULL,
  `ffdate` tinyint NOT NULL,
  `approvaldate` tinyint NOT NULL,
  `crit` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `criticality`
--

DROP TABLE IF EXISTS `criticality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `criticality` (
  `serviceId` int(11) unsigned NOT NULL,
  `flipExposed` tinyint(1) NOT NULL DEFAULT '0',
  `flipClosed` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`serviceId`),
  CONSTRAINT `FK_criticality_services` FOREIGN KEY (`serviceId`) REFERENCES `services` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_roman_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `exposed`
--

DROP TABLE IF EXISTS `exposed`;
/*!50001 DROP VIEW IF EXISTS `exposed`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `exposed` (
  `id` tinyint NOT NULL,
  `hostname` tinyint NOT NULL,
  `ip` tinyint NOT NULL,
  `port` tinyint NOT NULL,
  `product` tinyint NOT NULL,
  `version` tinyint NOT NULL,
  `extrainfo` tinyint NOT NULL,
  `lsdate` tinyint NOT NULL,
  `ffdate` tinyint NOT NULL,
  `crit` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `machinelog`
--

DROP TABLE IF EXISTS `machinelog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `machinelog` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `machineId` int(10) unsigned NOT NULL,
  `exposed` tinyint(1) unsigned NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`,`machineId`),
  KEY `FK__machines` (`machineId`),
  CONSTRAINT `FK__machines` FOREIGN KEY (`machineId`) REFERENCES `machines` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4241 DEFAULT CHARSET=utf8 COLLATE=utf8_roman_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `machines`
--

DROP TABLE IF EXISTS `machines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `machines` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hostname` char(200) COLLATE utf8_roman_ci DEFAULT NULL,
  `ip` char(15) COLLATE utf8_roman_ci NOT NULL,
  `rangeId` int(10) unsigned NOT NULL,
  `lsdate` datetime NOT NULL,
  `ffdate` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Schlüssel 2` (`ip`)
) ENGINE=InnoDB AUTO_INCREMENT=2440 DEFAULT CHARSET=utf8 COLLATE=utf8_roman_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `neatline`
--

DROP TABLE IF EXISTS `neatline`;
/*!50001 DROP VIEW IF EXISTS `neatline`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `neatline` (
  `id` tinyint NOT NULL,
  `serviceId` tinyint NOT NULL,
  `neat` tinyint NOT NULL,
  `justification` tinyint NOT NULL,
  `date` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `scanlog`
--

DROP TABLE IF EXISTS `scanlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scanlog` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `jobid` char(36) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `state` varchar(100) COLLATE utf8_roman_ci NOT NULL DEFAULT 'IN PROGRESS',
  `startdate` datetime NOT NULL,
  `enddate` datetime DEFAULT NULL,
  `output` varchar(20000) COLLATE utf8_roman_ci DEFAULT NULL,
  `iprange` varchar(200) COLLATE utf8_roman_ci DEFAULT NULL,
  `portrange` varchar(20) COLLATE utf8_roman_ci DEFAULT NULL,
  `extraoptions` varchar(300) COLLATE utf8_roman_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4261 DEFAULT CHARSET=utf8 COLLATE=utf8_roman_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `servicelog`
--

DROP TABLE IF EXISTS `servicelog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `servicelog` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `serviceId` int(10) unsigned NOT NULL,
  `openp` tinyint(1) unsigned NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`,`serviceId`),
  KEY `FK__services` (`serviceId`),
  CONSTRAINT `FK__services` FOREIGN KEY (`serviceId`) REFERENCES `services` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2887 DEFAULT CHARSET=utf8 COLLATE=utf8_roman_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `servicelogCur`
--

DROP TABLE IF EXISTS `servicelogCur`;
/*!50001 DROP VIEW IF EXISTS `servicelogCur`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `servicelogCur` (
  `serviceId` tinyint NOT NULL,
  `openp` tinyint NOT NULL,
  `date` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `port` mediumint(8) unsigned NOT NULL,
  `protocolId` tinyint(3) unsigned NOT NULL,
  `machineId` int(10) unsigned NOT NULL,
  `product` varchar(250) COLLATE utf8_roman_ci DEFAULT NULL,
  `extrainfo` varchar(250) COLLATE utf8_roman_ci DEFAULT NULL,
  `version` varchar(250) COLLATE utf8_roman_ci DEFAULT NULL,
  `lsdate` datetime NOT NULL,
  `ffdate` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Schlüssel 2` (`port`,`machineId`),
  KEY `serviceToMachine` (`machineId`),
  CONSTRAINT `serviceToMachine` FOREIGN KEY (`machineId`) REFERENCES `machines` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2562 DEFAULT CHARSET=utf8 COLLATE=utf8_roman_ci COMMENT='port, protocolId, machineId, product, extrainfo, version, lsdate, ffdate';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `closed`
--

/*!50001 DROP TABLE IF EXISTS `closed`*/;
/*!50001 DROP VIEW IF EXISTS `closed`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `closed` AS select `s`.`id` AS `id`,`m`.`hostname` AS `hostname`,`m`.`ip` AS `ip`,`s`.`port` AS `port`,`s`.`product` AS `product`,`s`.`version` AS `version`,`s`.`extrainfo` AS `extrainfo`,`n`.`justification` AS `justification`,`s`.`lsdate` AS `lsdate`,`s`.`ffdate` AS `ffdate`,`n`.`date` AS `approvaldate`,(not(coalesce(`c`.`flipClosed`,0))) AS `crit` from ((((`machines` `m` join `services` `s` on((`m`.`id` = `s`.`machineId`))) join `servicelogCur` `l` on((`s`.`id` = `l`.`serviceId`))) left join `criticality` `c` on((`s`.`id` = `c`.`serviceId`))) left join `neatline` `n` on((`n`.`serviceId` = `s`.`id`))) where ((`l`.`openp` = 0) and exists(select 1 from `neatline` where ((`neatline`.`neat` = 1) and (`s`.`machineId` = `m`.`id`) and (`neatline`.`serviceId` = `s`.`id`)))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `exposed`
--

/*!50001 DROP TABLE IF EXISTS `exposed`*/;
/*!50001 DROP VIEW IF EXISTS `exposed`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `exposed` AS select `s`.`id` AS `id`,`m`.`hostname` AS `hostname`,`m`.`ip` AS `ip`,`s`.`port` AS `port`,`s`.`product` AS `product`,`s`.`version` AS `version`,`s`.`extrainfo` AS `extrainfo`,`s`.`lsdate` AS `lsdate`,`s`.`ffdate` AS `ffdate`,`c`.`flipExposed` AS `crit` from (((`machines` `m` join `services` `s` on((`m`.`id` = `s`.`machineId`))) join `servicelogCur` `l` on((`s`.`id` = `l`.`serviceId`))) left join `criticality` `c` on((`s`.`id` = `c`.`serviceId`))) where ((`l`.`openp` = 1) and (not(exists(select 1 from `neatline` where ((`neatline`.`neat` = 1) and (`s`.`machineId` = `m`.`id`) and (`neatline`.`serviceId` = `s`.`id`)))))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `neatline`
--

/*!50001 DROP TABLE IF EXISTS `neatline`*/;
/*!50001 DROP VIEW IF EXISTS `neatline`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `neatline` AS select `l`.`id` AS `id`,`l`.`serviceId` AS `serviceId`,`l`.`neat` AS `neat`,`l`.`justification` AS `justification`,`l`.`date` AS `date` from `changelog` `l` where `l`.`id` in (select max(`changelog`.`id`) from `changelog` group by `changelog`.`serviceId`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `servicelogCur`
--

/*!50001 DROP TABLE IF EXISTS `servicelogCur`*/;
/*!50001 DROP VIEW IF EXISTS `servicelogCur`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50001 VIEW `servicelogCur` AS select `l`.`serviceId` AS `serviceId`,`l`.`openp` AS `openp`,`l`.`date` AS `date` from `servicelog` `l` where `l`.`id` in (select max(`servicelog`.`id`) from `servicelog` group by `servicelog`.`serviceId`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-01-02 14:34:32
