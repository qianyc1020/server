# coding=utf-8
import threading
import time

import grpc

import core.globalvar as gl
from core import config
from game.niuniu.command.game import roomover_cmd
from game.niuniu.mode.game_status import GameStatus
from game.niuniu.server.command import record_cmd
from game.niuniu.timeout import start_timeout
from mode.base.create_game_details import CreateGameDetails
from mode.base.rebate import Rebate
from mode.base.update_currency import UpdateCurrency
from protocol.base.base_pb2 import EXECUTE_ACTION, SETTLE_GAME, ASK_XIAZHUANG
from protocol.base.game_base_pb2 import RecExecuteAction, RecSettleSingle
from protocol.game import zhipai_pb2_grpc
from protocol.game.bairen_pb2 import BaiRenDealCardAction, BaiRenPlayerOneSetResult
from protocol.game.zhipai_pb2 import SettleData


def execute(room, messageHandle):
    rate = float(config.get("niuniu", "rate"))
    if room.gameStatus == GameStatus.PLAYING:
        room.sendBetScore(messageHandle)
        settleData = SettleData()
        i = 0
        for p in room.positions:
            userSettleData = settleData.userSettleData.add()
            userSettleData.userId = i
            userSettleData.cardlist.extend(p.cards)
            userSettleData.score = 1
            userSettleData.grab = 1
            i += 1
        conn = grpc.insecure_channel('127.0.0.1:50014')
        client = zhipai_pb2_grpc.ZhipaiStub(channel=conn)
        settleResult = client.settle(settleData)

        executeAction = RecExecuteAction()
        dealCardAction = BaiRenDealCardAction()
        dealCardAction.cards.extend(room.positions[0].cards)
        dealCardAction.cards.extend(room.positions[1].cards)
        dealCardAction.cards.extend(room.positions[2].cards)
        dealCardAction.cards.extend(room.positions[3].cards)
        dealCardAction.cards.extend(room.positions[4].cards)
        executeAction.data = dealCardAction.SerializeToString()
        messageHandle.broadcast_watch_to_gateway(EXECUTE_ACTION, executeAction, room)

        userScore = {}
        bankerWin = 0
        positionWin = [0, 0, 0, 0, 0]
        for u in settleResult.userSettleResule:
            win = u.win
            if u.win > 0:
                positionWin[u.userId] = 1
            elif u.win < 0:
                positionWin[u.userId] = 2
            if win != 0:
                position = room.positions[u.userId]
                for k in position.playScores:
                    bankerWin -= win * position.playScores[k]
                    if k in userScore:
                        userScore[k] += win * position.playScores[k]
                    else:
                        userScore[k] = win * position.playScores[k]

        scores = str(bankerWin if bankerWin <= 0 else int((bankerWin * (1 - rate))))
        users = str(room.banker)
        rebates = []
        dayingjia = 0
        dayingjiaScore = 0
        dashujia = 0
        dashujiaScore = 0
        update_currency = []
        game_details = []
        for k in userScore:
            if dayingjiaScore < userScore[k]:
                dayingjia = k
                dayingjiaScore = userScore[k]
            if dashujiaScore > userScore[k]:
                dashujia = k
                dashujiaScore = userScore[k]
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
                    game_details.append(CreateGameDetails(k, 10, str(room.roomNo), userwin, userScore[k] - userwin,
                                                          int(time.time())))
                if 0 < userScore[k] - userwin:
                    rebate = Rebate()
                    rebate.userId = k
                    rebate.card = userScore[k] - userwin
                    rebates.append(rebate)

        room.trend.append(positionWin)
        if len(room.trend) > 10:
            room.trend.remove(room.trend[0])
        room.updateTrend(messageHandle, 0)

        niuniuPlayerOneSetResult = BaiRenPlayerOneSetResult()
        dayingjiaSeat = room.getWatchSeatByUserId(dayingjia)
        if dayingjiaSeat is not None:
            room.dayingjia = dayingjia
            userInfo = niuniuPlayerOneSetResult.dayingjia
            userInfo.account = dayingjiaSeat.account
            userInfo.playerId = dayingjiaSeat.userId
            userInfo.headUrl = dayingjiaSeat.head
            userInfo.createTime = dayingjiaSeat.createDate
            userInfo.ip = dayingjiaSeat.ip
            userInfo.online = dayingjiaSeat.online
            userInfo.nick = dayingjiaSeat.nickname
            userInfo.ready = dayingjiaSeat.ready
            userInfo.score = dayingjiaSeat.score - dayingjiaSeat.playScore
            userInfo.sex = dayingjiaSeat.sex
            userInfo.totalCount = dayingjiaSeat.total_count
            userInfo.loc = i
            userInfo.consumeVip = dayingjiaSeat.level
            niuniuPlayerOneSetResult.dayingjiaScore = dayingjiaScore

        dashujiaSeat = room.getWatchSeatByUserId(dashujia)
        if dashujiaSeat is not None:
            userInfo = niuniuPlayerOneSetResult.dashujia
            userInfo.account = dashujiaSeat.account
            userInfo.playerId = dashujiaSeat.userId
            userInfo.headUrl = dashujiaSeat.head
            userInfo.createTime = dashujiaSeat.createDate
            userInfo.ip = dashujiaSeat.ip
            userInfo.online = dashujiaSeat.online
            userInfo.nick = dashujiaSeat.nickname
            userInfo.ready = dashujiaSeat.ready
            userInfo.score = dashujiaSeat.score - dashujiaSeat.playScore
            userInfo.sex = dashujiaSeat.sex
            userInfo.totalCount = dashujiaSeat.total_count
            userInfo.loc = i
            userInfo.consumeVip = dashujiaSeat.level
            niuniuPlayerOneSetResult.dashujiaScore = dashujiaScore
        for seat in room.seats:
            if seat.userId != room.banker:
                daerSettlePlayerInfo = niuniuPlayerOneSetResult.players.add()
                s = room.getWatchSeatByUserId(seat.userId)
                daerSettlePlayerInfo.playerId = s.userId
                daerSettlePlayerInfo.score = 0 if s.userId not in userScore else userScore[s.userId]
                daerSettlePlayerInfo.totalScore = s.score
                gl.get_v("serverlogger").logger.info('''%d结算后总分%d''' % (s.userId, s.score))

        daerSettlePlayerInfo = niuniuPlayerOneSetResult.players.add()
        banker = None
        if 1 != room.banker:
            bankerFinalWin = bankerWin if bankerWin <= 0 else int((bankerWin * (1 - rate)))
            if 0 != bankerFinalWin:
                update_currency.append(UpdateCurrency(bankerFinalWin, room.banker, room.roomNo))
                game_details.append(CreateGameDetails(room.banker, 10, str(room.roomNo), bankerFinalWin,
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
        recSettleSingle.allocId = 10
        recSettleSingle.curPlayCount = room.gameCount + 1
        recSettleSingle.time = int(time.time())

        for s in room.watchSeats:
            daerSettlePlayerInfo = None
            if room.getSeatByUserId(s.userId) is None and s.userId != room.banker:
                daerSettlePlayerInfo = niuniuPlayerOneSetResult.players.add()
                daerSettlePlayerInfo.playerId = s.userId
                daerSettlePlayerInfo.score = 0 if s.userId not in userScore else userScore[s.userId]
                daerSettlePlayerInfo.totalScore = s.score
                gl.get_v("serverlogger").logger.info('''%d结算后总分%d''' % (s.userId, s.score))

            recSettleSingle.content = niuniuPlayerOneSetResult.SerializeToString()
            messageHandle.send_to_gateway(SETTLE_GAME, recSettleSingle, s.userId)
            if daerSettlePlayerInfo is not None:
                niuniuPlayerOneSetResult.players.remove(daerSettlePlayerInfo)

        if banker is not None:
            banker.lianzhuang += 1
            if banker.lianzhuang >= int(config.get("niuniu", "maxBankerTimes")):
                room.xiazhuang = True
            elif room.bankerScore >= int(config.get("niuniu", "getBankerScore")):
                room.xiazhuang = True
                messageHandle.send_to_gateway(ASK_XIAZHUANG, None, room.banker)

        if len(userScore) > 0:
            record_cmd.execute(room, users, scores)
        e = gl.get_v(str(room.roomNo) + "sendthread")
        e.close()
        gl.get_v("play-handle")[str(room.roomNo)].close()
        del gl.get_v("play-handle")[str(room.roomNo)]
        gl.del_v(str(room.roomNo) + "sendthread")
        if 0 != len(room.watchSeats):
            room.clear()
            room.gameCount += 1
            levelSeat = []
            for s in room.seats:
                if s.score < room.leaveScore or not s.online:
                    levelSeat.append(s.userId)
            for l in levelSeat:
                room.exit(l, messageHandle)
            threading.Thread(target=start_timeout.execute, args=(room.roomNo, messageHandle,),
                             name='start_timeout').start()  # 线程对象.
        else:
            roomover_cmd.execute(room, messageHandle)
