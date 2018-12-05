# coding=utf-8
import traceback

import core.globalvar as gl
from game.jinhua.mode.game_status import GameStatus
from game.jinhua.mode.jinhua_room import JinhuaRoom
from protocol.base.base_pb2 import EXECUTE_ACTION
from protocol.base.game_base_pb2 import RecExecuteAction
from protocol.game.jinhua_pb2 import JinhuaLookCardAction


def execute(userId, message, messageHandle):
    redis = gl.get_v("redis")
    if redis.exists(str(userId) + "_room"):
        roomNo = redis.get(str(userId) + "_room")
        redis.lock("lockroom_" + str(roomNo), 5000)
        try:
            room = redis.getobj("room_" + str(roomNo), JinhuaRoom(), JinhuaRoom().object_to_dict)
            if room.gameStatus != GameStatus.PLAYING:
                gl.get_v("serverlogger").logger.info("看牌失败状态不对")
                redis.unlock("lockroom_" + str(roomNo))
                return
            seat = room.getSeatByUserId(userId)
            if seat is not None and not seat.lookCard and not seat.end:
                seat.lookCard = True
                recExecuteAction = RecExecuteAction()
                recExecuteAction.playerId = seat.userId
                for s in room.seats:
                    lookCardAction = JinhuaLookCardAction()
                    if s.userId == userId:
                        lookCardAction.cards.extend(s.initialCards)
                        room.historyActions.append(recExecuteAction.SerializeToString())
                    recExecuteAction.data = lookCardAction.SerializeToString()
                    messageHandle.send_to_gateway(EXECUTE_ACTION, recExecuteAction, s.userId)
                room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
