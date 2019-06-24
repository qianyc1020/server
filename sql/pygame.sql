DROP TABLE IF EXISTS `user_withdrawal`;
DROP TABLE IF EXISTS `user_rebate_to`;
DROP TABLE IF EXISTS `user_rebate`;
DROP TABLE IF EXISTS `account`;
DROP TABLE IF EXISTS `game_details`;
DROP TABLE IF EXISTS `gold`;
DROP TABLE IF EXISTS `match_record`;
DROP TABLE IF EXISTS `t_logger`;
DROP TABLE IF EXISTS `t_notice`;
DROP TABLE IF EXISTS `t_recharge`;
DROP TABLE IF EXISTS `user_bankcard`;
DROP TABLE IF EXISTS `user_ipinfo`;
DROP TABLE IF EXISTS `user_phone_number`;
DROP TABLE IF EXISTS `user_total_consumption`;



INSERT INTO `t_account` VALUES ('402880e76729fee501672a32d5e30004',184,'2018-11-19 12:20:34','admin','1eaca8b7f7128e85aba43181801d7921','7190a55ef2346dbf5917f8ad03965666','0:0:0:0:0:0:0:1','2019-06-09 00:47:56','Mac','','',1),('402880e76729fee501672a32d5e30005',12,'2018-11-19 12:20:34','user','1eaca8b7f7128e85aba43181801d7921','7190a55ef2346dbf5917f8ad03965666','127.0.0.1','2019-06-09 00:37:26','Mac','1','',1);

INSERT INTO `t_user` VALUES ('402880e76729fee501672a32d5e30004',NULL,'admin',0.00,_binary '\0',1,NULL,NULL,10000,0.00,0.00,NULL,NULL,10000.00,NULL,NULL,NULL),('402880e76729fee501672a32d5e30005',NULL,'user',1.00,_binary '\0',1,NULL,NULL,10000,0.00,0.00,NULL,NULL,10000.00,NULL,NULL,NULL);

INSERT INTO `t_permission` VALUES ('402880e76729fee501672a3606350006',6,'2018-11-19 12:24:03','system','系统配置修改','/system/**',1),('4028828f6b37dbc4016b37e50c070000',0,'2019-06-09 00:21:26','account','账户管理','/account/**',1),('4028828f6b37dbc4016b37e614610002',0,'2019-06-09 00:22:34','gameuser','游戏用户管理','/gameuser/**',1),('4028828f6b37dbc4016b37e6a3000004',0,'2019-06-09 00:23:10','gold','游戏余额','/gold/**',1),('4028828f6b37dbc4016b37e723930006',0,'2019-06-09 00:23:43','notice','公告管理','/notice/**',1),('4028828f6b37dbc4016b37e7baf50008',0,'2019-06-09 00:24:22','permission','权限管理','/permission/**',1),('4028828f6b37dbc4016b37e82092000a',0,'2019-06-09 00:24:48','role','角色管理','/role/**',1),('4028828f6b37dbc4016b37e8ad32000c',0,'2019-06-09 00:25:24','withdrawal','提现管理','/withdrawal/**',1),('4028828f6b37dbc4016b37e989a4000e',0,'2019-06-09 00:26:20','userparent','用户关系管理','/userparent/**',1),('4028828f6b37ec11016b37f629a20002',0,'2019-06-09 00:40:08','recharge','充值管理','/recharge/**',1);

INSERT INTO `t_role` VALUES ('402880e76729fee501672a30766a0000',9,'2018-11-19 12:17:58','user','用户总后台',1),('402880e76729fee501672a3673580008',7,'2018-11-19 12:24:31','admin','超级管理',1);

INSERT INTO `t_account_role` VALUES ('402880e76729fee501672a32d5e30005','402880e76729fee501672a30766a0000'),('402880e76729fee501672a32d5e30004','402880e76729fee501672a3673580008');

INSERT INTO `t_sequence` VALUES ('e79067ed6b2e17ec016b360a0c5e0008',1);

INSERT INTO `t_recharge_select` VALUES ('1',0,NULL,1,9.98,0,998,_binary '\0'),('2',0,NULL,1,49.50,0,4950,_binary '\0'),('3',0,NULL,1,99.80,0,9980,_binary '\0'),('4',0,NULL,1,198.00,0,19800,_binary '\0'),('5',0,NULL,1,495.00,0,49500,_binary '\0'),('6',0,NULL,1,995.00,0,99500,_binary '\0'),('7',0,NULL,1,1995.00,0,199500,_binary '\0'),('8',0,NULL,1,5995.00,0,599500,_binary '\0'),('9',0,NULL,1,9995.00,0,999500,_binary '\0');

INSERT INTO `t_system` VALUES ('1',1,'2018-11-19 12:19:21','0.00',0.00,0,NULL,0.00,'0','0','1',NULL,NULL,0,1.00);

INSERT INTO pygame.account (id, account_name, nick_name, sex, head_url, pswd, create_time, last_time, last_address, account_state, gold, integral, bank_pswd, bank_gold, bank_integral, authority, total_count, introduce, phone, level, experience) VALUES (10000, '10000', _binary '10000', 1, '', 'b7a782741f667201b54880c925faec4b', 1544611319, 1544780348, '127.0.0.1:34279', 0, 0.00, 0.00, null, 0.00, 0.00, 0, 0, null, null, 0, 0);
INSERT INTO pygame.account (id, account_name, nick_name, sex, head_url, pswd, create_time, last_time, last_address, account_state, gold, integral, bank_pswd, bank_gold, bank_integral, authority, total_count, introduce, phone, level, experience) VALUES (10001, '10001', _binary '10001', 1, '', 'd89f3a35931c386956c1a402a8e09941', 1544611319, 1544780348, '127.0.0.1:34279', 0, 0.00, 0.00, null, 0.00, 0.00, 0, 0, null, null, 0, 0);
INSERT INTO pygame.account (id, account_name, nick_name, sex, head_url, pswd, create_time, last_time, last_address, account_state, gold, integral, bank_pswd, bank_gold, bank_integral, authority, total_count, introduce, phone, level, experience) VALUES (10002, '10002', _binary '10002', 1, '', '9103c8c82514f39d8360c7430c4ee557', 1544611319, 1544780348, '127.0.0.1:34279', 0, 0.00, 0.00, null, 0.00, 0.00, 0, 0, null, null, 0, 0);
INSERT INTO pygame.account (id, account_name, nick_name, sex, head_url, pswd, create_time, last_time, last_address, account_state, gold, integral, bank_pswd, bank_gold, bank_integral, authority, total_count, introduce, phone, level, experience) VALUES (10003, '10003', _binary '10003', 1, '', 'f5dffc111454b227fbcdf36178dfe6ac', 1544611319, 1544780348, '127.0.0.1:34279', 0, 0.00, 0.00, null, 0.00, 0.00, 0, 0, null, null, 0, 0);
INSERT INTO pygame.account (id, account_name, nick_name, sex, head_url, pswd, create_time, last_time, last_address, account_state, gold, integral, bank_pswd, bank_gold, bank_integral, authority, total_count, introduce, phone, level, experience) VALUES (10004, '10004', _binary '10004', 1, '', 'd783823cc6284b929c2cd8df2167d212', 1544611319, 1544780348, '127.0.0.1:34279', 0, 0.00, 0.00, null, 0.00, 0.00, 0, 0, null, null, 0, 0);
INSERT INTO pygame.account (id, account_name, nick_name, sex, head_url, pswd, create_time, last_time, last_address, account_state, gold, integral, bank_pswd, bank_gold, bank_integral, authority, total_count, introduce, phone, level, experience) VALUES (10005, '10005', _binary '10005', 1, '', '6eb887126d24e8f1cd8ad5033482c781', 1544611319, 1544780348, '127.0.0.1:34279', 0, 0.00, 0.00, null, 0.00, 0.00, 0, 0, null, null, 0, 0);

INSERT INTO `user_rebate` VALUES (1,1,'2018-12-12 17:24:24',10000,NULL,NULL,10000,0.00,0.00,1.00);
INSERT INTO `user_rebate` VALUES (2,1,'2018-12-12 17:24:24',10001,NULL,NULL,10001,0.00,0.00,1.00);
INSERT INTO `user_rebate` VALUES (3,1,'2018-12-12 17:24:24',10002,NULL,NULL,10002,0.00,0.00,1.00);
INSERT INTO `user_rebate` VALUES (4,1,'2018-12-12 17:24:24',10003,NULL,NULL,10003,0.00,0.00,1.00);
INSERT INTO `user_rebate` VALUES (5,1,'2018-12-12 17:24:24',10004,NULL,NULL,10004,0.00,0.00,1.00);
INSERT INTO `user_rebate` VALUES (6,1,'2018-12-12 17:24:24',10005,NULL,NULL,10005,0.00,0.00,1.00);
ALTER TABLE user_rebate AUTO_INCREMENT = 100;