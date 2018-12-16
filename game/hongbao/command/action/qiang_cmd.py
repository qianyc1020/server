# coding=utf-8
import traceback

import core.globalvar as gl
from game.hongbao.command.game import gameover_cmd
from game.hongbao.mode.hongbao_room import HongbaoRoom
from protocol.game.hongbao_pb2 import BaiRenHongbaoQiang


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    qiang = BaiRenHongbaoQiang()
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo), HongbaoRoom(), HongbaoRoom().object_to_dict)
            if room.started and room.banker != userId and userId not in room.userScore:
                s = room.getWatchSeatByUserId(userId)
                if s is not None:
                    score = room.hongbaolist[0]
                    room.hongbaolist.remove(score)

                    qiang.score = score
                    userInfo = qiang.user
                    userInfo.account = s.account
                    userInfo.playerId = s.userId
                    userInfo.headUrl = s.head
                    userInfo.createTime = s.createDate
                    userInfo.ip = s.ip
                    userInfo.online = s.online
                    userInfo.nick = s.nickname
                    userInfo.ready = s.ready
                    userInfo.score = s.score - s.playScore
                    userInfo.sex = s.sex
                    userInfo.totalCount = s.total_count
                    userInfo.loc = 0
                    userInfo.consumeVip = s.level
                    room.executeAction(userId, 2, qiang, messageHandle)
                    room.userScore[userId] = score
                    if 0 == len(room.hongbaolist):
                        gameover_cmd.execute(room, messageHandle)
                    room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
