# coding=utf-8
import traceback

import core.globalvar as gl
from game.douniu.mode.game_status import GameStatus
from game.douniu.mode.douniu_room import DouniuRoom
from protocol.base.base_pb2 import REENTER_GAME
from protocol.base.game_base_pb2 import RecReEnterGame


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")

        gameid = redis.get(str(roomNo) + "_gameId")
        if 2 != gameid:
            return

        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), DouniuRoom(), DouniuRoom().object_to_dict)
            seat = room.getSeatByUserId(userId)
            if seat is not None:
                recReEnterGame = RecReEnterGame()
                recReEnterGame.gameState = room.gameStatus
                recReEnterGame.state = True
                recReEnterGame.curPlayCount = room.gameCount
                messageHandle.send_to_gateway(REENTER_GAME, recReEnterGame)

                room.recUpdateGameInfo(messageHandle)
                room.recUpdateScore(messageHandle, 0)

                if room.gameStatus != GameStatus.WAITING:
                    room.recReEnterGameInfo(messageHandle, userId)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
