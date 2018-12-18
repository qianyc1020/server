# coding=utf-8
import traceback

from core import config
from data.database import mysql_connection


def create_game_details(details):
    connection = None
    try:
        connection = mysql_connection.get_conn()
        with connection.cursor() as cursor:
            for d in details:
                sql = config.get("sql", "sql_game_details") % (
                d.user_id, d.alloc_id, d.room_no, d.score, d.service_charge, d.time)
                cursor.execute(sql)
            connection.commit()
    except:
        print traceback.print_exc()
        if connection is not None:
            connection.rollback()
    finally:
        if connection is not None:
            connection.close()
