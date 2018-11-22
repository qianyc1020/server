# coding=utf-8
import threading
import time

import grpc

import core.globalvar as gl
from core import config
from game.tuitongzi.command.game import roomover_cmd
from game.tuitongzi.mode.game_status import GameStatus
from game.tuitongzi.timeout import start_timeout
from game.tuitongzi.server.command import record_cmd
from protocol.base.base_pb2 import EXECUTE_ACTION, SETTLE_GAME, ASK_XIAZHUANG
from protocol.base.game_base_pb2 import RecExecuteAction, RecSettleSingle
from protocol.game import zhipai_pb2_grpc
from protocol.game.bairen_pb2 import BaiRenDealCardAction, BaiRenPlayerOneSetResult
from protocol.game.zhipai_pb2 import SettleData


def execute(room, messageHandle):
    rate = float(config.get("tuitongzi", "rate"))
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
        conn = grpc.insecure_channel('127.0.0.1:50013')
        client = zhipai_pb2_grpc.ZhipaiStub(channel=conn)
        settleResult = client.settle(settleData)

        executeAction = RecExecuteAction()
        dealCardAction = BaiRenDealCardAction()
        dealCardAction.cards.append(room.positions[0].cards[1])
        dealCardAction.cards.append(room.positions[1].cards[1])
        dealCardAction.cards.append(room.positions[2].cards[1])
        dealCardAction.cards.append(room.positions[3].cards[1])
        executeAction.data = dealCardAction.SerializeToString()
        messageHandle.broadcast_watch_to_gateway(EXECUTE_ACTION, executeAction, room)

        userScore = {}
        bankerWin = 0
        tuitongziPlayerOneSetResult = BaiRenPlayerOneSetResult()
        tuitongziPlayerOneSetResult.positionWin.append(0)
        tuitongziPlayerOneSetResult.positionWin.append(0)
        tuitongziPlayerOneSetResult.positionWin.append(0)
        tuitongziPlayerOneSetResult.positionWin.append(0)

        for u in settleResult.userSettleResule:
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

        scores = str(bankerWin if bankerWin <= 0 else int((bankerWin * (1 - rate))))
        users = str(room.banker)

        dayingjia = 0
        dayingjiaScore = 0
        dashujia = 0
        dashujiaScore = 0
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
                    messageHandle.game_update_currency(userwin, k, room.roomNo)
                # TODO 经验值和返利

        room.trend.append(tuitongziPlayerOneSetResult.positionWin)
        if len(room.trend) > 20:
            room.trend.remove(room.trend[0])
        room.updateTrend(messageHandle, 0)

        dayingjiaSeat = room.getWatchSeatByUserId(dayingjia)
        if dayingjiaSeat is not None:
            room.dayingjia = dayingjia
            userInfo = tuitongziPlayerOneSetResult.dayingjia
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
            tuitongziPlayerOneSetResult.dayingjiaScore = dayingjiaScore

        dashujiaSeat = room.getWatchSeatByUserId(dashujia)
        if dashujiaSeat is not None:
            userInfo = tuitongziPlayerOneSetResult.dashujia
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
            tuitongziPlayerOneSetResult.dashujiaScore = dashujiaScore
        for seat in room.seats:
            if seat.userId != room.banker:
                daerSettlePlayerInfo = tuitongziPlayerOneSetResult.players.add()
                s = room.getWatchSeatByUserId(seat.userId)
                daerSettlePlayerInfo.playerId = s.userId
                daerSettlePlayerInfo.score = 0 if s.userId not in userScore else userScore[s.userId]
                daerSettlePlayerInfo.totalScore = s.score
                gl.get_v("serverlogger").logger.info('''%d结算后总分%d''' % (s.userId, s.score))

        daerSettlePlayerInfo = tuitongziPlayerOneSetResult.players.add()
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
        recSettleSingle.allocId = 7
        recSettleSingle.curPlayCount = room.gameCount + 1
        recSettleSingle.time = int(time.time())

        for s in room.watchSeats:
            daerSettlePlayerInfo = None
            if room.getSeatByUserId(s.userId) is None and s.userId != room.banker:
                daerSettlePlayerInfo = tuitongziPlayerOneSetResult.players.add()
                daerSettlePlayerInfo.playerId = s.userId
                daerSettlePlayerInfo.score = 0 if s.userId not in userScore else userScore[s.userId]
                daerSettlePlayerInfo.totalScore = s.score
                gl.get_v("serverlogger").logger.info('''%d结算后总分%d''' % (s.userId, s.score))

            recSettleSingle.content = tuitongziPlayerOneSetResult.SerializeToString()
            messageHandle.send_to_gateway(SETTLE_GAME, recSettleSingle, s.userId)
            if daerSettlePlayerInfo is not None:
                tuitongziPlayerOneSetResult.players.remove(daerSettlePlayerInfo)

        if banker is not None:
            if room.bankerScore >= int(config.get("tuitongzi", "getBankerScore")):
                room.xiazhuang = True
                messageHandle.send_to_gateway(ASK_XIAZHUANG, None, room.banker)

        if len(userScore) > 0:
            record_cmd.execute(room, users, scores)
        e = gl.get_v(str(room.roomNo) + "sendthread")
        e.close()
        gl.del_v(str(room.roomNo) + "sendthread")
        if 0 != len(room.watchSeats):
            room.clear()
            room.gameCount += 1
            t = threading.Thread(target=start_timeout.execute, args=(room.roomNo, messageHandle,),
                                 name='handle')  # 线程对象.
            t.start()
        else:
            roomover_cmd.execute(room, messageHandle)
