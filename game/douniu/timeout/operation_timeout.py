import time
import traceback

import core.globalvar as gl
from game.douniu.mode.game_status import GameStatus
from protocol.game.douniu_pb2 import DouniuScoreAction, DouniuCardAction


def execute(roomNo, messageHandle, gameStatus, gameCount):
    time.sleep(10)

    redis = gl.get_v("redis")
    if redis.exists("room_" + str(roomNo)):
        redis.lock("lockroom_" + str(roomNo))
        try:
            room = redis.getobj("room_" + str(roomNo))
            if room.gameCount == gameCount and room.gameStatus == gameStatus:
                if gameStatus == GameStatus.GRABING:
                    for seat in room.seats:
                        if -1 == seat.grab and not seat.guanzhan:
                            seat.grab = 0
                            room.executeAction(seat.userId, 1, DouniuScoreAction(), messageHandle)
                    room.checkGrab(messageHandle)
                elif gameStatus == GameStatus.PLAYING:
                    for seat in room.seats:
                        if -1 == seat.playScore and not seat.guanzhan and seat.userId != room.banker:
                            seat.playScore = room.betType * room.score
                            douniuScoreAction = DouniuScoreAction()
                            douniuScoreAction.score = seat.playScore
                            room.executeAction(seat.userId, 2, douniuScoreAction, messageHandle)
                    room.checkPlay(messageHandle)
                elif gameStatus == GameStatus.OPENING:
                    for seat in room.seats:
                        if not seat.openCard and not seat.guanzhan:
                            seat.openCard = True
                            douniuCardAction = DouniuCardAction()
                            douniuCardAction.cards.extend(seat.initialCards)
                            room.executeAction(seat.userId, 3, douniuCardAction, messageHandle)
                    room.checkOpen(messageHandle)
                room.save(redis)
        except:
            print traceback.print_exc()
        redis.unlock("lockroom_" + str(roomNo))
