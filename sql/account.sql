DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account` (
  `id`            INT(11) PRIMARY KEY                      NOT NULL UNIQUE,
  `account_name`  VARCHAR(128) COLLATE utf8mb4_unicode_ci  NOT NULL UNIQUE,
  `nick_name`     BLOB,
  `sex`           INT(11)                                           DEFAULT 0,
  `head_url`      VARCHAR(255) COLLATE utf8mb4_unicode_ci           DEFAULT NULL,
  `pswd`          VARCHAR(255) COLLATE utf8mb4_unicode_ci,
  `create_time`   INT(10) UNSIGNED                                  DEFAULT 0,
  `last_time`     INT(10) UNSIGNED                                  DEFAULT 0,
  `last_address`  VARCHAR(255) COLLATE utf8mb4_unicode_ci,
  `account_state` INT(11)                                           DEFAULT 0,
  `gold`          DECIMAL(19, 2)                                    DEFAULT 0,
  `integral`      DECIMAL(19, 2)                                    DEFAULT 0,
  `bank_pswd`     VARCHAR(255) COLLATE utf8mb4_unicode_ci,
  `bank_gold`     DECIMAL(19, 2)                                    DEFAULT 0,
  `bank_integral` DECIMAL(19, 2)                                    DEFAULT 0,
  `authority`     INT(10) UNSIGNED                                  DEFAULT 0,
  `total_count`   INT(10) UNSIGNED                                  DEFAULT 0,
  `introduce`     VARCHAR(1024)                                     DEFAULT NULL,
  `phone`         VARCHAR(255)                                      DEFAULT NULL,
  `level`         INT(11) UNSIGNED                                  DEFAULT 0,
  `experience`    BIGINT(19)                                        DEFAULT 0,
  `device`        VARCHAR(255)                                      DEFAULT NULL

)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;
ALTER TABLE account
  AUTO_INCREMENT = 10000;
INSERT INTO pygame.account (10000, account_name, nick_name, sex, head_url, pswd, create_time, last_time, last_address, account_state, gold, integral, bank_pswd, bank_gold, bank_integral, authority, total_count, introduce, phone, level, experience) VALUES ('pengyi', 0x70656E677969, 1, '', '54292b463c3e765a42d20d4f76d38c91', 1544611319, 1544780348, '127.0.0.1:34279', 0, 0.00, 0.00, null, 0.00, 0.00, 0, 0, null, null, 0, 0);