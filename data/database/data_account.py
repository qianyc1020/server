# coding=utf-8
import time

from core import config
from data.database import mysql_connection
from mode.account import Account
from utils.stringutils import StringUtils


def login(loginserver, address):
    t = time.time()
    connection = None
    try:
        connection = mysql_connection.get_conn()

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
        connection = mysql_connection.get_conn()

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
        a.bank_pswd = result["bank_pswd"]
        a.bank_gold = result["bank_gold"]
        a.bank_integral = result["bank_integral"]
        a.authority = result["authority"]
        a.total_count = result["total_count"]
        a.introduce = result["introduce"]
        a.phone = result["phone"]
        a.level = result["level"]
        a.experience = result["experience"]

        return a


def query_account_by_id(connection, id):
    sql = config.get("sql", "sql_query_account_by_id") % id
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
        a.bank_pswd = result["bank_pswd"]
        a.bank_gold = result["bank_gold"]
        a.bank_integral = result["bank_integral"]
        a.authority = result["authority"]
        a.total_count = result["total_count"]
        a.introduce = result["introduce"]
        a.phone = result["phone"]
        a.level = result["level"]
        a.experience = result["experience"]

        return a


def update_currency(connection, gold, integral, id):
    sql = config.get("sql", "sql_update_currency") % (-gold, -integral, gold, integral, id)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()
