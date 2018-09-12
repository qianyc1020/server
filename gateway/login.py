# coding=utf-8
import time

import pymysql

from gateway.mode.account import Account
from utils.stringutils import StringUtils


def login(loginserver, address):
    t = time.time()
    connection = None
    try:
        connection = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     password='Pengyi_9627',
                                     db='pygame',
                                     charset='utf8mb4',
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
        connection = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     password='Pengyi_9627',
                                     db='pygame',
                                     charset='utf8mb4',
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
    sql = '''INSERT INTO account (account_name, nick_name, sex, head_url, pswd, create_time, last_time, last_address, account_state, gold, integral, records, authority, total_count) VALUES ("%s", "%s", %d, "%s", "%s", %d, %d, "%s", %d, %d, %d, "%s", %d, %d)''' % (
        loginserver.account, loginserver.nick, loginserver.sex, loginserver.headUrl, StringUtils.md5(
            loginserver.account), int(t), int(t), address, 0, 0, 0, '', 0, 0)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()


def update_login_with_info(t, connection, loginserver, address):
    sql = '''UPDATE account SET nick_name = "%s", sex = %d, head_url="%s", last_time=%d, last_address="%s" WHERE account_name = "%s"''' % (
        loginserver.nick, loginserver.sex, loginserver.headUrl, int(t), address, loginserver.account)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()


def update_login(t, connection, address, account):
    sql = '''UPDATE account SET last_time=%d, last_address="%s" WHERE account_name = "%s"''' % (
        int(t), address, account)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()


def exist_account(connection, account):
    sql = '''SELECT COUNT(id) AS result FROM account WHERE account_name = "%s"''' % account
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result["result"] != 0


def query_account_by_account(connection, account):
    sql = '''SELECT * FROM account WHERE account_name = "%s"''' % account
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
