# coding=utf-8
import traceback

import core.globalvar as gl
from core import config
from game.hongbao.command.game import gamestart_cmd
from game.hongbao.mode.game_status import GameStatus
from game.hongbao.mode.hongbao_room import HongbaoRoom
from protocol.game.bairen_pb2 import BaiRenScore


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), HongbaoRoom(), HongbaoRoom().object_to_dict)
            seat = room.getWatchSeatByUserId(userId)
            if seat is None or room.banker == userId:
                redis.unlock("lockroom_" + str(roomNo))
                return
            score = BaiRenScore()
            score.ParseFromString(message.data)
            if 1 == len(score.score):
                seat.shangzhuangScore = score.score[0]
                room.bankerList.append(userId)
                room.updateBankerList(messageHandle, 0)
                if bool(config.get("hongbao",
                                   "onlyPlayerBanker")) and room.gameStatus == GameStatus.WAITING and 1 == room.banker:
                    gamestart_cmd.execute(room, messageHandle)
            redis.setobj("room_" + str(roomNo), room)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
