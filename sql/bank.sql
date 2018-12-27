DROP TABLE IF EXISTS `bank`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bank`
(
  `id`   INT(11) PRIMARY KEY                    NOT NULL AUTO_INCREMENT UNIQUE,
  `name` VARCHAR(32) COLLATE utf8mb4_unicode_ci NOT NULL
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;