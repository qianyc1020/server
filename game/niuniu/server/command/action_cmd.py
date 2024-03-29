# coding=utf-8
from game.niuniu.command.action import playscore_cmd
from protocol.base.game_base_pb2 import ReqSendAction


def execute(userId, message, messageHandle):
    action = ReqSendAction()
    action.ParseFromString(message.data)
    if 2 == action.actionType:
        playscore_cmd.execute(userId, action.data, messageHandle)
