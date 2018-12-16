# coding=utf-8
from game.hongbao.command.action import selnum_cmd, qiang_cmd
from protocol.base.game_base_pb2 import ReqSendAction


def execute(userId, message, messageHandle):
    action = ReqSendAction()
    action.ParseFromString(message.data)
    if 1 == action.actionType:
        selnum_cmd.execute(userId, action.data, messageHandle)
    elif 2 == action.actionType:
        qiang_cmd.execute(userId, action.data, messageHandle)
