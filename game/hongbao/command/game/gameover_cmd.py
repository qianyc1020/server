# coding=utf-8
import threading
import time

import core.globalvar as gl
from core import config
from game.hongbao.command.game import roomover_cmd
from game.hongbao.mode.game_status import GameStatus
from game.hongbao.timeout import start_timeout
from game.hongbao.server.command import record_cmd
from protocol.base.base_pb2 import SETTLE_GAME, ASK_XIAZHUANG
from protocol.base.game_base_pb2 import RecSettleSingle
from protocol.game.bairen_pb2 import BaiRenPlayerOneSetResult


def execute(room, messageHandle):
    rate = float(config.get("hongbao", "rate"))
    if room.gameStatus == GameStatus.PLAYING:

        userScore = {}
        bankerWin = 0
        hongbaoPlayerOneSetResult = BaiRenPlayerOneSetResult()

        for (d, x) in room.userScore.items():
            win = 0
            if x % 10 == room.selectNum:
                win = -room.bankerScore + x
            else:
                win = x
            userScore[int(d)] = win
            bankerWin -= win

        scores = str(bankerWin if bankerWin <= 0 else int((bankerWin * (1 - rate))))
        users = str(room.banker)

        for k in userScore:
            seat = room.getWatchSeatByUserId(k)
            if seat is not None:
                gl.get_v("serverlogger").logger.info('''%d下注前%d''' % (k, seat.score))
                gl.get_v("serverlogger").logger.info('''%d下注%d''' % (k, seat.playScore))
                gl.get_v("serverlogger").logger.info('''%d输赢%d''' % (k, userScore[k]))
                userwin = userScore[k] if userScore[k] <= 0 else int((userScore[k] * (1 - rate)))
                seat.score += userwin
                scores += "," + str(userwin)
                users += "," + str(k)
                if 0 != userwin:
                    messageHandle.game_update_currency(userwin, k, room.roomNo)
                # TODO 经验值和返利

        for (d, x) in userScore.items():
            daerSettlePlayerInfo = hongbaoPlayerOneSetResult.players.add()
            s = room.getWatchSeatByUserId(d)
            daerSettlePlayerInfo.playerId = s.userId
            daerSettlePlayerInfo.score = x
            daerSettlePlayerInfo.totalScore = s.score
            gl.get_v("serverlogger").logger.info('''%d结算后总分%d''' % (d, s.score))

        daerSettlePlayerInfo = hongbaoPlayerOneSetResult.players.add()
        banker = None
        if 1 != room.banker:
            bankerFinalWin = bankerWin if bankerWin <= 0 else int((bankerWin * (1 - rate)))
            if 0 != bankerFinalWin:
                messageHandle.game_update_currency(bankerFinalWin, room.banker, room.roomNo)
            banker = room.getWatchSeatByUserId(room.banker)
            room.bankerScore += bankerFinalWin
            banker.shangzhuangScore = room.bankerScore
            if banker is not None:
                banker.score += bankerFinalWin
                daerSettlePlayerInfo.totalScore = banker.score
            # TODO 经验值和返利
        # TODO else 系统输赢
        daerSettlePlayerInfo.playerId = room.banker
        daerSettlePlayerInfo.score = bankerWin

        recSettleSingle = RecSettleSingle()
        recSettleSingle.allocId = 11
        recSettleSingle.curPlayCount = room.gameCount + 1
        recSettleSingle.time = int(time.time())

        for s in room.watchSeats:
            daerSettlePlayerInfo = None
            if room.getSeatByUserId(s.userId) is None and s.userId != room.banker:
                daerSettlePlayerInfo = hongbaoPlayerOneSetResult.players.add()
                daerSettlePlayerInfo.playerId = s.userId
                daerSettlePlayerInfo.score = 0 if s.userId not in userScore else userScore[s.userId]
                daerSettlePlayerInfo.totalScore = s.score
                gl.get_v("serverlogger").logger.info('''%d结算后总分%d''' % (s.userId, s.score))

            recSettleSingle.content = hongbaoPlayerOneSetResult.SerializeToString()
            messageHandle.send_to_gateway(SETTLE_GAME, recSettleSingle, s.userId)
            if daerSettlePlayerInfo is not None:
                hongbaoPlayerOneSetResult.players.remove(daerSettlePlayerInfo)

        if banker is not None:
            if room.bankerScore >= int(config.get("hongbao", "getBankerScore")):
                room.xiazhuang = True
                messageHandle.send_to_gateway(ASK_XIAZHUANG, None, room.banker)

        if len(userScore) > 0:
            record_cmd.execute(room, users, scores)
        if 0 != len(room.watchSeats):
            room.clear()
            room.gameCount += 1
            t = threading.Thread(target=start_timeout.execute, args=(room.roomNo, messageHandle,),
                                 name='handle')  # 线程对象.
            t.start()
        else:
            roomover_cmd.execute(room, messageHandle)
