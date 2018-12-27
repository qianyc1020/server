DROP TABLE IF EXISTS `bank_card`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bank_card`
(
  `id`        INT(11) PRIMARY KEY                    NOT NULL AUTO_INCREMENT UNIQUE,
  `bank_name` VARCHAR(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rel_name`  VARCHAR(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_no`  VARCHAR(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bank_No`   VARCHAR(32) COLLATE utf8mb4_unicode_ci NOT NULL
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;