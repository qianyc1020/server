DROP TABLE IF EXISTS `game_details`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_details`
(
  `id`             INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
  `user_id`        INT(11) NOT NULL,
  `alloc_id`       INT(11) NOT NULL,
  `room_no`        VARCHAR(32),
  `score`          DECIMAL(19, 2),
  `service_charge` DECIMAL(19, 2),
  `time`           INT(11) UNSIGNED NOT NULL
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;