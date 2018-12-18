# coding=utf-8
import traceback
from Queue import Empty

import core.globalvar as gl
from data.database import data_game_details


class GameDetailsHandle(object):

    def __init__(self):
        self.__close = False

    def close(self):
        self.__close = True

    def handle(self, queue):
        while not self.__close:
            try:
                details = queue.getall(20, True, 20)
                data_game_details.create_game_details(details)
            except Empty:
                gl.get_v("serverlogger").logger.info("Received timeout")
            except:
                print traceback.print_exc()
