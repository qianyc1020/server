DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account` (
  `id`            INT(11) PRIMARY KEY                      NOT NULL AUTO_INCREMENT UNIQUE,
  `account_name`  VARCHAR(128) COLLATE utf8mb4_unicode_ci  NOT NULL UNIQUE,
  `nick_name`     BLOB,
  `sex`           INT(11)                                           DEFAULT 0,
  `head_url`      VARCHAR(255) COLLATE utf8mb4_unicode_ci           DEFAULT NULL,
  `pswd`          VARCHAR(255) COLLATE utf8mb4_unicode_ci,
  `create_time`   INT(10) UNSIGNED                                  DEFAULT NULL,
  `last_time`     INT(10) UNSIGNED                                  DEFAULT NULL,
  `last_address`  VARCHAR(255) COLLATE utf8mb4_unicode_ci,
  `account_state` INT(11)                                           DEFAULT 0,
  `gold`          DECIMAL(19, 2)                                    DEFAULT NULL,
  `integral`      DECIMAL(19, 2)                                    DEFAULT NULL,
  `bank_pswd`     VARCHAR(255) COLLATE utf8mb4_unicode_ci,
  `bank_gold`     DECIMAL(19, 2)                                    DEFAULT NULL,
  `bank_integral` DECIMAL(19, 2)                                    DEFAULT NULL,
  `records`       VARCHAR(4096) COLLATE utf8mb4_unicode_ci          DEFAULT NULL,
  `authority`     INT(10) UNSIGNED                                  DEFAULT NULL,
  `total_count`   INT(10) UNSIGNED                                  DEFAULT NULL,
  `introduce`     VARCHAR(1024)                                     DEFAULT NULL,
  `phone`         VARCHAR(255)                                      DEFAULT NULL,
  `level`         INT(11) UNSIGNED                                  DEFAULT 0,
  `experience`    BIGINT(19)                                        DEFAULT 0

)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;
ALTER TABLE account
  AUTO_INCREMENT = 10000;