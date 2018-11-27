# coding=utf-8
from game.douniu.command.action import playscore_cmd, grab_cmd, open_cmd
from protocol.base.game_base_pb2 import ReqSendAction


def execute(userId, message, messageHandle):
    action = ReqSendAction()
    action.ParseFromString(message.data)
    if 1 == action.actionType:
        grab_cmd.execute(userId, action.data, messageHandle)
    if 2 == action.actionType:
        playscore_cmd.execute(userId, action.data, messageHandle)
    if 3 == action.actionType:
        open_cmd.execute(userId, action.data, messageHandle)
