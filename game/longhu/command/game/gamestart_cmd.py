# coding=utf-8

import core.globalvar as gl
from core import config
from game.longhu.command.game import dealcard_cmd
from game.longhu.mode.game_status import GameStatus
from protocol.base.base_pb2 import LEAVE_BANKER


def execute(room, messageHandle):
    if room.gameStatus == GameStatus.WAITING:
        banker = room.getWatchSeatByUserId(room.banker)
        if (1 != room.banker and room.xiazhuang) or (
                banker is not None and banker.shangzhuangScore < int(config.get("longhu", "getBankerScore"))):
            messageHandle.broadcast_watch_to_gateway(LEAVE_BANKER, None, room)
        if bool(config.get("longhu", "onlyPlayerBanker")) and 0 == len(room.bankerList) and (
                1 == room.banker or room.xiazhuang or banker is None or room.bankerScore < int(
            config.get("longhu", "getBankerScore"))):
            gl.get_v("serverlogger").logger.info('''开始游戏-无庄''')
            room.banker = 1
            return

        room.seats = []
        if len(room.watchSeats) < 6:
            room.seats.extend(room.watchSeats[0: len(room.watchSeats)])
        else:
            room.seats.extend(room.watchSeats[0: 6])
        room.recUpdateScore(messageHandle, 0)
        room.bankerConfirm(messageHandle)
        if bool(config.get("longhu", "onlyPlayerBanker")) and 1 == room.banker:
            gl.get_v("serverlogger").logger.info('''开始游戏-无庄''')
            return
        dealcard_cmd.execute(room, messageHandle)
