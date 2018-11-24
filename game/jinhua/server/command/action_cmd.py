# coding=utf-8
from game.jinhua.command.action import playscore_cmd, look_cmd, abandon_cmd, compare_cmd
from protocol.base.game_base_pb2 import ReqSendAction


def execute(userId, message, messageHandle):
    action = ReqSendAction()
    action.ParseFromString(message.data)
    if 0 == action.actionType:
        look_cmd.execute(userId, action.data, messageHandle)
    if 1 == action.actionType:
        abandon_cmd.execute(userId, action.data, messageHandle)
    if 2 == action.actionType:
        playscore_cmd.execute(userId, action.data, messageHandle)
    if 3 == action.actionType:
        compare_cmd.execute(userId, action.data, messageHandle)
