# coding=utf-8
import pymysql

from core import config


def get_conn():
    return pymysql.connect(host=config.get("db", "db_host"),
                           port=int(config.get("db", "db_port")),
                           user=config.get("db", "db_user"),
                           password=config.get("db", "db_pass"),
                           db=config.get("db", "db_db"),
                           charset=config.get("db", "db_charset"),
                           cursorclass=pymysql.cursors.DictCursor)
