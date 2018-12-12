# coding=utf-8
import traceback

from core import config
from data.database import mysql_connection


def create_user_rebate(create_date, user_id):
    connection = None
    try:
        connection = mysql_connection.get_conn()
        sql = config.get("sql", "sql_user_rebate") % (0, create_date, user_id, 10000, "", 10000, 0, 0, 0)
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
