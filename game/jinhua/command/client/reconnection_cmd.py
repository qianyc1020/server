# coding=utf-8
import traceback

import core.globalvar as gl
from game.jinhua.mode.game_status import GameStatus
from protocol.base.base_pb2 import REENTER_GAME
from protocol.base.game_base_pb2 import RecReEnterGame


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")

        gameid = redis.get(str(roomNo) + "_gameId")
        if 1 != gameid:
            return

        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
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
