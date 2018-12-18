# coding=utf-8
import threading
import time

import core.globalvar as gl
from core import config
from game.hongbao.command.game import roomover_cmd
from game.hongbao.mode.game_status import GameStatus
from game.hongbao.server.command import record_cmd
from game.hongbao.timeout import start_timeout
from mode.base.create_game_details import CreateGameDetails
from mode.base.rebate import Rebate
from mode.base.update_currency import UpdateCurrency
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
        rebates = []
        update_currency = []
        game_details = []
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
                    update_currency.append(UpdateCurrency(userwin, k, room.roomNo))
                    game_details.append(CreateGameDetails(k, 11, str(room.roomNo), userwin, userScore[k] - userwin,
                                                          int(time.time())))
                    if 0 < userScore[k] - userwin:
                        rebate = Rebate()
                        rebate.userId = k
                        rebate.card = userScore[k] - userwin
                        rebates.append(rebate)

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
                update_currency.append(UpdateCurrency(bankerFinalWin, room.banker, room.roomNo))
                game_details.append(CreateGameDetails(room.banker, 11, str(room.roomNo), bankerFinalWin,
                                                      bankerWin - bankerFinalWin, int(time.time())))
                if 0 < bankerWin - bankerFinalWin:
                    rebate = Rebate()
                    rebate.userId = room.banker
                    rebate.card = bankerWin - bankerFinalWin
                    rebates.append(rebate)
            banker = room.getWatchSeatByUserId(room.banker)
            room.bankerScore += bankerFinalWin
            banker.shangzhuangScore = room.bankerScore
            if banker is not None:
                banker.score += bankerFinalWin
                daerSettlePlayerInfo.totalScore = banker.score
        if 0 < len(rebates):
            gl.get_v("rebate-handle-queue").put(rebates)
        if 0 != len(update_currency):
            gl.get_v("update_currency").putall(update_currency)
        if 0 != len(game_details):
            gl.get_v("game_details").putall(game_details)
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
            threading.Thread(target=start_timeout.execute, args=(room.roomNo, messageHandle,),
                             name='start_timeout').start()  # 线程对象.
        else:
            roomover_cmd.execute(room, messageHandle)
