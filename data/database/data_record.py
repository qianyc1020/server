# coding=utf-8
import time
import traceback

from core import config
from data.database import mysql_connection, data_account
from mode.base.record import Record
from protocol.service.match_pb2 import RecMatchRecordInfo


def create_record(id, alloc_id, room_no, game, players, scores, time):
    connection = None
    try:
        connection = mysql_connection.get_conn()
        sql = config.get("sql", "sql_create_record") % (id, alloc_id, room_no, game, players, scores, time)
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


def get_records(allocIds, __userId):
    connection = None
    recMatchRecordInfo = RecMatchRecordInfo()
    try:
        connection = mysql_connection.get_conn()
        records = []
        ps = []
        t = int(time.time())
        in_p = ""
        for a in allocIds:
            in_p += "," + str(a)
        sql = config.get("sql", "sql_get_record") % (str((t - 259200) * 1000000), "%" + str(__userId) + "%", in_p[1:])
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            for r in result:
                a = Record()
                a.id = r["id"]
                a.alloc_id = r["alloc_id"]
                a.roomNo = r["room_no"]
                a.players = r["players"]
                a.scores = r["scores"]
                a.time = r["time"]
                records.append(a)
                playes = a.players.split(",")
                for p in playes:
                    if p not in ps:
                        ps.append(p)
        if len(ps) > 0:
            accounts = data_account.query_account_by_ids(connection, ps)

            for r in records:
                recordInfos = recMatchRecordInfo.matchRecords.add()
                recordInfos.recordId = r.id
                recordInfos.allocId = r.alloc_id
                recordInfos.playTime = r.time
                recordInfos.gameId = int(r.roomNo)

                rplayers = r.players.split(",")
                rscore = r.scores.split(",")

                for i in range(0, len(rplayers)):
                    playerDatas = recordInfos.playerDatas.add()
                    playerDatas.playerId = int(rplayers[i])
                    if 1 == int(rplayers[i]):
                        playerDatas.nick = "系统"
                    else:
                        playerDatas.nick = accounts[int(rplayers[i])].nick_name
                    playerDatas.score = int(rscore[i])
    except:
        print traceback.print_exc()
    finally:
        if connection is not None:
            connection.close()
    return recMatchRecordInfo
