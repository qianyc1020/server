# coding=utf-8
import time
import traceback

from core import config
from data.database import mysql_connection
from mode.base.account import Account
from utils.http_utils import HttpUtils
from utils.stringutils import StringUtils


def login(loginserver, address):
    connection = None
    account = None
    try:
        connection = mysql_connection.get_conn()

        if not exist_account(connection, loginserver.account):
            create_account(time.time(), connection, loginserver, address)
            gold = int(config.get("gateway", "login_give"))
            account = query_account_by_account(connection, loginserver.account)
            # data_user_rebate.create_user_rebate(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), account.id)
            s = HttpUtils(config.get("api", "api_host")).get(
                config.get("api", "bind") % (account.id, loginserver.higher, address.split(':')[0]),
                None)
            res = s.read()
            if 0 != gold:
                update_currency(connection, gold, 0, 0, 0, account.id)
        account = query_account_by_account(connection, loginserver.account)
    except:
        if connection is not None:
            connection.rollback()
        print traceback.print_exc()
    finally:
        if connection is not None:
            connection.close()
    return account


def relogin(relogininfo, address):
    t = time.time()
    connection = None
    try:
        connection = mysql_connection.get_conn()

        if exist_account(connection, relogininfo.account):
            update_login(t, connection, address, relogininfo.account)
        return query_account_by_account(connection, relogininfo.account)
    except:
        if connection is not None:
            connection.rollback()
        print traceback.print_exc()
    finally:
        if connection is not None:
            connection.close()
    return None


def create_account(t, connection, loginserver, address):
    close = connection is None
    try:
        if connection is None:
            connection = mysql_connection.get_conn()
        sql = config.get("sql", "sql_create_account") % (
            loginserver.account, StringUtils.phoneToNick(loginserver.nick), loginserver.sex,
            loginserver.headUrl, StringUtils.md5(loginserver.account), int(t),
            # config.get("gateway", "head_url") % random.randint(1, 50), StringUtils.md5(loginserver.account), int(t),
            int(t), address, 0, 0, 0, '', 0, 0, loginserver.device)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
    except:
        if close and connection is not None:
            connection.rollback()
        print traceback.print_exc()
    finally:
        if close and connection is not None:
            connection.close()


def update_login_with_info(t, connection, loginserver, address, device):
    close = connection is None
    try:
        if connection is None:
            connection = mysql_connection.get_conn()
        sql = config.get("sql", "sql_update_login_with_info") % (
            StringUtils.phoneToNick(loginserver.nick), loginserver.sex, loginserver.headUrl, int(t), address, device,
            loginserver.account)
        # StringUtils.phoneToNick(loginserver.nick), loginserver.sex, int(t), address, device, loginserver.account)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
    except:
        if close and connection is not None:
            connection.rollback()
        print traceback.print_exc()
    finally:
        if close and connection is not None:
            connection.close()


def update_login(t, connection, address, account, device):
    close = connection is None
    try:
        if connection is None:
            connection = mysql_connection.get_conn()
        sql = config.get("sql", "sql_update_login") % (int(t), address, device, account)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
    except:
        if close and connection is not None:
            connection.rollback()
        print traceback.print_exc()
    finally:
        if close and connection is not None:
            connection.close()


def exist_account(connection, account):
    close = connection is None
    try:
        if connection is None:
            connection = mysql_connection.get_conn()
        sql = config.get("sql", "sql_exist_account") % account
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            return result["result"] != 0
    except:
        print traceback.print_exc()
    finally:
        if close and connection is not None:
            connection.close()
    return False


def query_account_by_account(connection, account):
    close = connection is None
    try:
        if connection is None:
            connection = mysql_connection.get_conn()
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
            a.device = result["device"]
            return a
    except:
        print traceback.print_exc()
    finally:
        if close and connection is not None:
            connection.close()
    return None


def query_account_by_id(connection, id):
    close = connection is None
    try:
        if connection is None:
            connection = mysql_connection.get_conn()
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
            a.device = result["device"]
            return a
    except:
        print traceback.print_exc()
    finally:
        if close and connection is not None:
            connection.close()
    return None


def query_account_by_ids(connection, ids):
    close = connection is None
    accounts = {}
    try:
        if connection is None:
            connection = mysql_connection.get_conn()
        in_p = ', '.join((map(lambda x: '%s', ids)))
        sql = config.get("sql", "sql_query_account_by_ids") % in_p
        with connection.cursor() as cursor:
            cursor.execute(sql, ids)
            r = cursor.fetchall()
            for result in r:
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
                a.device = result["device"]
                accounts[a.id] = a
    except:
        print traceback.print_exc()
    finally:
        if close and connection is not None:
            connection.close()
    return accounts


def update_currency(connection, gold, integral, bankGold, bankIntegral, id):
    close = connection is None
    try:
        if connection is None:
            connection = mysql_connection.get_conn()
        sql = config.get("sql", "sql_update_currency") % (gold, integral, bankGold, bankIntegral, id)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
    except:
        if close and connection is not None:
            connection.rollback()
        print traceback.print_exc()
    finally:
        if close and connection is not None:
            connection.close()


def update_currencys(updates):
    connection = None
    try:
        connection = mysql_connection.get_conn()
        with connection.cursor() as cursor:
            for update in updates:
                sql = config.get("sql", "sql_update_currency") % (update.gold, 0, 0, 0, update.user_id)
                cursor.execute(sql)
            connection.commit()
    except:
        if connection is not None:
            connection.rollback()
        print traceback.print_exc()
    finally:
        if connection is not None:
            connection.close()


def update_introduce(connection, id, content):
    account = None
    close = connection is None
    try:
        if connection is None:
            connection = mysql_connection.get_conn()
        sql = config.get("sql", "sql_update_introduce") % (content, id)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
        account = query_account_by_id(connection, id)
    except:
        if close and connection is not None:
            connection.rollback()
        print traceback.print_exc()
    finally:
        if close and connection is not None:
            connection.close()
    return account


def ranking_by_gold(connection, limit):
    close = connection is None
    try:
        if connection is None:
            connection = mysql_connection.get_conn()
        accounts = []
        sql = config.get("sql", "sql_ranking_by_gold") % limit
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            for r in result:
                a = Account()
                a.id = r["id"]
                a.account_name = r["account_name"]
                a.nick_name = r["nick_name"]
                a.sex = r["sex"]
                a.pswd = r["pswd"]
                a.head_url = r["head_url"]
                a.create_time = r["create_time"]
                a.last_time = r["last_time"]
                a.last_address = r["last_address"]
                a.account_state = r["account_state"]
                a.gold = r["gold"]
                a.integral = r["integral"]
                a.bank_pswd = r["bank_pswd"]
                a.bank_gold = r["bank_gold"]
                a.bank_integral = r["bank_integral"]
                a.authority = r["authority"]
                a.total_count = r["total_count"]
                a.introduce = r["introduce"]
                a.phone = r["phone"]
                a.level = r["level"]
                a.experience = r["experience"]
                a.device = r["device"]
                accounts.append(a)
            return accounts
    except:
        print traceback.print_exc()
    finally:
        if close and connection is not None:
            connection.close()
    return None
