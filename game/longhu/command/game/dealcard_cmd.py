# coding=utf-8
import threading
import time
import traceback

import grpc

import core.globalvar as gl
from game.longhu.command.game import gameover_cmd
from game.longhu.handle.playscore_handle import PlayScoreHandle
from game.longhu.mode.game_status import GameStatus
from game.longhu.timeout import play_timeout
from game.longhu.timeout.send_scores_timeout import SendScores
from protocol.base.base_pb2 import EXECUTE_ACTION
from protocol.base.game_base_pb2 import RecExecuteAction
from protocol.game import zhipai_pb2_grpc
from protocol.game.zhipai_pb2 import ShuffleData
from utils.TestQueue import TestQueue


def execute(room, messageHandle):
    try:
        if room.gameStatus == GameStatus.WAITING:
            shuffleData = ShuffleData()
            conn = grpc.insecure_channel('127.0.0.1:50011')
            client = zhipai_pb2_grpc.ZhipaiStub(channel=conn)
            shuffleResult = client.shuffle(shuffleData)
            cardlist = shuffleResult.cardlist
            room.positions[0].cards.append(cardlist[0])
            room.positions[1].cards.append(cardlist[1])
            room.startDate = int(time.time())
        if room.gameStatus == GameStatus.PLAYING:
            gameover_cmd.execute(room, messageHandle)
        else:
            executeAction = RecExecuteAction()
            executeAction.actionType = 0
            messageHandle.broadcast_watch_to_gateway(EXECUTE_ACTION, executeAction, room)
            room.gameStatus = GameStatus.PLAYING
            room.historyActions.append(executeAction.SerializeToString())
            room.executeAsk(messageHandle, 0, 2)
            threading.Thread(target=play_timeout.execute, args=(room.roomNo, messageHandle, room.gameCount,),
                             name='play_timeout').start()  # 线程对象.
            gl.get_v("serverlogger").logger.info("开始下注")
            playHandle = PlayScoreHandle(str(room.roomNo), TestQueue())
            gl.get_v("play-handle")[str(room.roomNo)] = playHandle
            threading.Thread(target=playHandle.execute, name='playthread').start()  # 线程对象.

            if gl.get_v(str(room.roomNo) + "sendthread") is None:
                e = SendScores(room.roomNo, messageHandle)
                threading.Thread(target=e.execute, name='sendthread').start()  # 线程对象.
                gl.set_v(str(room.roomNo) + "sendthread", e)
    except:
        print traceback.print_exc()
