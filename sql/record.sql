DROP TABLE IF EXISTS `match_record`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `match_record` (
  `id`       VARCHAR(32) PRIMARY KEY                      NOT NULL UNIQUE,
  `alloc_id` INT(11)                                      NOT NULL,
  `room_no`  VARCHAR(32),
  `game`     BLOB(10240),
  `players`  VARCHAR(5120) COLLATE utf8mb4_unicode_ci    NOT NULL,
  `scores`   VARCHAR(5120) COLLATE utf8mb4_unicode_ci,
  `time`     INT(11) UNSIGNED                             NOT NULL
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;