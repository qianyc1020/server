INSERT INTO pygame.account (id, account_name, nick_name, sex, head_url, pswd, create_time, last_time, last_address, account_state, gold, integral, bank_pswd, bank_gold, bank_integral, authority, total_count, introduce, phone, level, experience) VALUES (10000, '10000', _binary '10000', 1, '', 'b7a782741f667201b54880c925faec4b', 1544611319, 1544780348, '127.0.0.1:34279', 0, 0.00, 0.00, null, 0.00, 0.00, 0, 0, null, null, 0, 0);
INSERT INTO `t_account` VALUES ('402880e76729fee501672a32d5e30004',184,'2018-11-19 12:20:34','admin','1eaca8b7f7128e85aba43181801d7921','7190a55ef2346dbf5917f8ad03965666','0:0:0:0:0:0:0:1','2019-06-09 00:47:56','Mac','','',1),('402880e76729fee501672a32d5e30005',12,'2018-11-19 12:20:34','user','1eaca8b7f7128e85aba43181801d7921','7190a55ef2346dbf5917f8ad03965666','127.0.0.1','2019-06-09 00:37:26','Mac','1','',1);

INSERT INTO `t_account_role` VALUES ('402880e76729fee501672a32d5e30005','402880e76729fee501672a30766a0000'),('402880e76729fee501672a32d5e30004','402880e76729fee501672a3673580008');

INSERT INTO `t_permission` VALUES ('402880e76729fee501672a3606350006',6,'2018-11-19 12:24:03','system','系统配置修改','/system/**',1),('4028828f6b37dbc4016b37e50c070000',0,'2019-06-09 00:21:26','account','账户管理','/account/**',1),('4028828f6b37dbc4016b37e614610002',0,'2019-06-09 00:22:34','gameuser','游戏用户管理','/gameuser/**',1),('4028828f6b37dbc4016b37e6a3000004',0,'2019-06-09 00:23:10','gold','游戏余额','/gold/**',1),('4028828f6b37dbc4016b37e723930006',0,'2019-06-09 00:23:43','notice','公告管理','/notice/**',1),('4028828f6b37dbc4016b37e7baf50008',0,'2019-06-09 00:24:22','permission','权限管理','/permission/**',1),('4028828f6b37dbc4016b37e82092000a',0,'2019-06-09 00:24:48','role','角色管理','/role/**',1),('4028828f6b37dbc4016b37e8ad32000c',0,'2019-06-09 00:25:24','withdrawal','提现管理','/withdrawal/**',1),('4028828f6b37dbc4016b37e989a4000e',0,'2019-06-09 00:26:20','userparent','用户关系管理','/userparent/**',1),('4028828f6b37ec11016b37f629a20002',0,'2019-06-09 00:40:08','recharge','充值管理','/recharge/**',1);

INSERT INTO `t_recharge_select` VALUES ('1',0,NULL,1,1.00,0,100,_binary '\0'),('2',0,NULL,1,500.00,0,50000,_binary '\0');

INSERT INTO `t_role` VALUES ('402880e76729fee501672a30766a0000',9,'2018-11-19 12:17:58','user','用户总后台',1),('402880e76729fee501672a3673580008',7,'2018-11-19 12:24:31','admin','超级管理',1);

INSERT INTO `t_sequence` VALUES ('e79067ed6b2e17ec016b360a0c5e0008',1);

INSERT INTO `t_system` VALUES ('1',1,'2018-11-19 12:19:21','0.00',0.00,0,NULL,0.00,'0','0','1',NULL,NULL,0,1.00);

INSERT INTO `t_user` VALUES ('402880e76729fee501672a32d5e30004',NULL,'admin',0.00,_binary '\0',1,NULL,NULL,10000,0.00,0.00,NULL,NULL,10000.00,NULL,NULL,NULL),('402880e76729fee501672a32d5e30005',NULL,'user',1.00,_binary '\0',1,NULL,NULL,10000,0.00,0.00,NULL,NULL,10000.00,NULL,NULL,NULL);

INSERT INTO `user_rebate` VALUES (1,1,'2018-12-12 17:24:24',10000,NULL,NULL,10000,0.00,0.00,1.00);
ALTER TABLE user_rebate AUTO_INCREMENT = 100;