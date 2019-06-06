# coding=utf-8
import pkg_resources

from core import config
import core.globalvar as gl
from protocol.game.zhipai_pb2 import ShuffleData

config.init("./conf/pyg.conf")
gl.init()

from game.tuitongzi.server.server import Server

if __name__ == '__main__':
    with open('./conf/tuitongzicheat.t') as infile:
        strs = infile.read()
        str = strs.split(',')

        shuffleData = ShuffleData()
        cheatData = shuffleData.cheatData.add()
        cheatData.level = int(str[0])
        cheatData = shuffleData.cheatData.add()
        cheatData.level = int(str[1])
        cheatData = shuffleData.cheatData.add()
        cheatData.level = int(str[2])
        cheatData = shuffleData.cheatData.add()
        cheatData.level = int(str[3])
