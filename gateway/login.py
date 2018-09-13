# coding=utf-8
import time

import pymysql

from core import config
from gateway.mode.account import Account
from utils.stringutils import StringUtils


def login(loginserver, address):
    t = time.time()
    connection = None
    try:
        connection = pymysql.connect(host=config.get("db", "db_host"),
                                     port=int(config.get("db", "db_port")),
                                     user=config.get("db", "db_user"),
                                     password=config.get("db", "db_pass"),
                                     db=config.get("db", "db_db"),
                                     charset=config.get("db", "db_charset"),
                                     cursorclass=pymysql.cursors.DictCursor)

        if not exist_account(connection, loginserver.account):
            create_account(t, connection, loginserver, address)
        else:
            if loginserver.nick is not None:
                update_login_with_info(t, connection, loginserver, address)
            else:
                update_login(t, connection, address, loginserver.account)
        return query_account_by_account(connection, loginserver.account)
    except BaseException, e:
        if connection is not None:
            connection.rollback()
        print e
    finally:
        if connection is not None:
            connection.close()
    return None


def relogin(relogininfo, address):
    t = time.time()
    connection = None
    try:
        connection = pymysql.connect(host=config.get("db", "db_host"),
                                     port=int(config.get("db", "db_port")),
                                     user=config.get("db", "db_user"),
                                     password=config.get("db", "db_pass"),
                                     db=config.get("db", "db_db"),
                                     charset=config.get("db", "db_charset"),
                                     cursorclass=pymysql.cursors.DictCursor)

        if exist_account(connection, relogininfo.account):
            update_login(t, connection, address, relogininfo.account)
        return query_account_by_account(connection, relogininfo.account)
    except BaseException, e:
        if connection is not None:
            connection.rollback()
        print e
    finally:
        if connection is not None:
            connection.close()
    return None


def create_account(t, connection, loginserver, address):
    sql = config.get("sql", "sql_create_account") % (
        loginserver.account, loginserver.nick, loginserver.sex, loginserver.headUrl, StringUtils.md5(
            loginserver.account), int(t), int(t), address, 0, 0, 0, '', 0, 0)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()


def update_login_with_info(t, connection, loginserver, address):
    sql = config.get("sql", "sql_update_login_with_info") % (
        loginserver.nick, loginserver.sex, loginserver.headUrl, int(t), address, loginserver.account)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()


def update_login(t, connection, address, account):
    sql = config.get("sql", "sql_update_login") % (int(t), address, account)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()


def exist_account(connection, account):
    sql = config.get("sql", "sql_exist_account") % account
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result["result"] != 0


def query_account_by_account(connection, account):
    sql = config.get("sql", "sql_query_account_by_account") % account
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()
        a = Account()
        a.id = result["id"]
        a.account_name = result["account_name"]
        a.nick_name = result["nick_name"]
        a.sex = result["sex"]
        a.pswd = result["pswd"]
        a.head_url = result["head_url"]
        a.create_time = result["create_time"]
        a.last_time = result["last_time"]
        a.last_address = result["last_address"]
        a.account_state = result["account_state"]
        a.gold = result["gold"]
        a.integral = result["integral"]
        a.authority = result["authority"]
        a.total_count = result["total_count"]
        a.introduce = result["introduce"]
        a.phone = result["phone"]
        a.level = result["level"]
        a.experience = result["experience"]

        return a
