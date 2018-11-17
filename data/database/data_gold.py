# coding=utf-8
import time
import traceback

from core import config
from data.database import mysql_connection


def create_gold(type, source, user_id, gold):
    from data.database import data_account
    connection = None
    try:
        connection = mysql_connection.get_conn()

        account = data_account.query_account_by_id(connection, user_id)
        sql = config.get("sql", "sql_create_gold") % (type, source, user_id, gold, account.gold, int(time.time()))
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
    except:
        print traceback.print_exc()
        if connection is not None:
            connection.rollback()
    finally:
        if connection is not None:
            connection.close()
