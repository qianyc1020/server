# coding=utf-8
import time
from decimal import Decimal

import grpc

import core.globalvar as gl
from core import config
from data.database import data_account
from game.longhu.mode.game_status import GameStatus
from protocol.base.base_pb2 import EXECUTE_ACTION, SETTLE_GAME, ASK_XIAZHUANG
from protocol.base.game_base_pb2 import RecExecuteAction, RecUpdateGameUsers, RecSettleSingle
from protocol.game import zhipai_pb2_grpc
from protocol.game.longfeng_pb2 import BaiRenLongFengDealCardAction, BaiRenLongFengPlayerOneSetResult
from protocol.game.zhipai_pb2 import SettleData


def execute(room, messageHandle):
    rate = float(config.get("longhu", "rate"))
    if room.gameStatus == GameStatus.PLAYING:
        room.sendBetScore(messageHandle)
        settleData = SettleData()
        i = 0
        for p in room.positions:
            userSettleData = settleData.userSettleData.Add()
            userSettleData.userId = i
            userSettleData.cardlist.extend(p.cards)
            userSettleData.score = 1
            userSettleData.grab = 1
            i += 1
        conn = grpc.insecure_channel('127.0.0.1:50011')
        client = zhipai_pb2_grpc.ZhipaiStub(channel=conn)
        settleResult = client.settle(settleData)

        executeAction = RecExecuteAction()
        dealCardAction = BaiRenLongFengDealCardAction()
        dealCardAction.cards.append(room.positions[0].cards[0])
        dealCardAction.cards.append(room.positions[1].cards[0])
        executeAction.data = dealCardAction.SerializeToString()
        messageHandle.broadcast_watch_to_gateway(EXECUTE_ACTION, executeAction, room)

        userScore = {}
        bankerWin = 0
        tuitongziPlayerOneSetResult = BaiRenLongFengPlayerOneSetResult()
        tuitongziPlayerOneSetResult.positionWin.append(0)
        tuitongziPlayerOneSetResult.positionWin.append(0)
        tuitongziPlayerOneSetResult.positionWin.append(0)

        for u in settleResult.userSettleResuleList:
            win = 0
            if u.win > 0:
                win = 1
                tuitongziPlayerOneSetResult.positionWin[u.userId] = 1
            elif u.win < 0:
                win = -1
                tuitongziPlayerOneSetResult.positionWin[u.userId] = 2
            if win != 0:
                position = room.positions[u.userId]
                for k in position.playScores:
                    bankerWin -= win * position.playScores[k]
                    if userScore.has_key(k):
                        userScore[k] += win * position.playScores[k]
                    else:
                        userScore[k] = win * position.playScores[k]

        win = 0
        if 0 == settleResult.userSettleResuleList[0].win:
            win = 10
            tuitongziPlayerOneSetResult.positionWin[2] = 1
        else:
            win = -1
            tuitongziPlayerOneSetResult.positionWin[2] = 2

        for k in room.positions[2].playScores:
            bankerWin -= win * room.positions[2].playScores[k]
            if userScore.has_key(k):
                userScore[k] += win * room.positions[2].playScores[k]
            else:
                userScore[k] = win * room.positions[2].playScores[k]

        pingReturn = float(config.get("longhu", "pingReturn"))
        if 1 != pingReturn:
            if 0 == settleResult.userSettleResuleList[0].win:
                win = -1
                for k in room.positions[0].playScores:
                    bankerWin -= win * room.positions[0].playScores[k]
                    if userScore.has_key(k):
                        userScore[k] += win * room.positions[0].playScores[k]
                    else:
                        userScore[k] = win * room.positions[0].playScores[k]
                for k in room.positions[1].playScores:
                    bankerWin -= win * room.positions[1].playScores[k]
                    if userScore.has_key(k):
                        userScore[k] += win * room.positions[1].playScores[k]
                    else:
                        userScore[k] = win * room.positions[1].playScores[k]

        scores = ""
        scores.join(",").join(str(bankerWin if bankerWin <= 0 else int((bankerWin * (1 - rate)))))
        users = ""
        users.join(",").join(str(room.banker))

        dayingjia = 0
        dayingjiaScore = 0
        for k in userScore:
            if dayingjiaScore < userScore[k]:
                dayingjia = k
                dayingjiaScore = userScore[k]
            seat = room.getWatchSeatByUserId(k)
            if seat is not None:
                gl.get_v("serverlogger").logger('''%d下注前%d''' % (k, seat.score))
                gl.get_v("serverlogger").logger('''%d下注%d''' % (k, seat.playScore))
                gl.get_v("serverlogger").logger('''%d输赢%d''' % (k, userScore[k]))
                userwin = userScore[k] if userScore[k] <= 0 else int((userScore[k] * (1 - rate)))
                seat.score += userwin
                scores.join(",").join(str(userwin))
                users.join(",").join(str(k))
                data_account.update_currency(None, userwin, 0, 0, 0, k)
                # TODO 经验值和返利

        room.trend.append(tuitongziPlayerOneSetResult.positionWin)
        if len(room.trend) > 20:
            room.trend.remove(room.trend[0])
        room.updateTrend(messageHandle, 0)

        dayingjiaSeat = room.getWatchSeatByUserId(dayingjia)
        if dayingjiaSeat is not None:
            room.dayingjia = dayingjia
            userInfo = RecUpdateGameUsers.UserInfo()
            userInfo.account = dayingjiaSeat.account
            userInfo.playerId = dayingjiaSeat.userId
            userInfo.headUrl = dayingjiaSeat.head
            userInfo.createTime = dayingjiaSeat.createDate
            userInfo.ip = dayingjiaSeat.ip
            userInfo.online = dayingjiaSeat.online
            userInfo.nick = dayingjiaSeat.nickname
            userInfo.ready = dayingjiaSeat.ready
            userInfo.score = int((dayingjiaSeat.score - dayingjiaSeat.playScore).quantize(Decimal('0')))
            userInfo.sex = dayingjiaSeat.sex
            userInfo.totalCount = dayingjiaSeat.total_count
            userInfo.loc = i
            userInfo.consumeVip = dayingjiaSeat.level
            tuitongziPlayerOneSetResult.dayingjia = userInfo
        for seat in room.seats:
            if seat.userId != room.banker:
                daerSettlePlayerInfo = tuitongziPlayerOneSetResult.players.Add()
                s = room.getWatchSeatByUserId(seat.userId)
                daerSettlePlayerInfo.playerId = s.userId
                daerSettlePlayerInfo.score = 0 if s.userId not in userScore else userScore[s.userId]
                daerSettlePlayerInfo.totalScore = s.score
                gl.get_v("serverlogger").logger('''%d结算后总分%d''' % (s.userId, s.score))

        daerSettlePlayerInfo = tuitongziPlayerOneSetResult.players.Add()
        banker = None
        if 1 != room.banker:
            bankerFinalWin = bankerWin if bankerWin <= 0 else int((bankerWin * (1 - rate)))
            data_account.update_currency(None, bankerFinalWin, 0, 0, 0, room.banker)
            banker = room.getWatchSeatByUserId(room.banker)
            room.bankerScore += bankerFinalWin
            banker.shangzhuangScore = room.bankerScore
            if banker is not None:
                banker.score += bankerFinalWin
                daerSettlePlayerInfo.total = banker.score
            # TODO 经验值和返利
        # TODO else 系统输赢
        daerSettlePlayerInfo.playerId = room.banker
        daerSettlePlayerInfo.score = bankerWin

        recSettleSingle = RecSettleSingle()
        recSettleSingle.allocId = 8
        recSettleSingle.curPlayCount = room.gameCount + 1
        recSettleSingle.time = int(time.time())

        for s in room.watchSeats:
            daerSettlePlayerInfo = None
            if room.getSeatByUserId(s.userId) is None and s.userId != room.banker:
                daerSettlePlayerInfo = tuitongziPlayerOneSetResult.players.Add()
                daerSettlePlayerInfo.playerId = s.userId
                daerSettlePlayerInfo.score = 0 if s.userId not in userScore else userScore[s.userId]
                daerSettlePlayerInfo.totalScore = s.score
                gl.get_v("serverlogger").logger('''%d结算后总分%d''' % (s.userId, s.score))

            recSettleSingle.content = tuitongziPlayerOneSetResult.SerializeToString()
            messageHandle.sendToPlayer(SETTLE_GAME, recSettleSingle, s.userId)
            if daerSettlePlayerInfo is not None:
                tuitongziPlayerOneSetResult.players.remove(daerSettlePlayerInfo)

        if banker is not None:
            if room.bankerScore >= int(config.get("longhu", "getBankerScore")):
                room.xiazhuang = True
                messageHandle.sendToPlayer(ASK_XIAZHUANG, None, room.banker)

        # TODO 战绩
        if 0 != len(room.watchSeats):
            room.clear()
            room.gameCount += 1
            # TODO 计时器 下一局开始
        # else:
        # TODO  roomOver
