# coding=utf-8
import traceback

from core import config
from data.database import mysql_connection


def create_game_details(user_id, alloc_id, room_no, score, service_charge, time):
    connection = None
    try:
        connection = mysql_connection.get_conn()
        sql = config.get("sql", "sql_game_details") % (user_id, alloc_id, room_no, score, service_charge, time)
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
