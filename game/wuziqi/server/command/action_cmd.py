# coding=utf-8
from game.wuziqi.command.action import set_amount_confirm_cmd
from protocol.base.game_base_pb2 import ReqSendAction


def execute(userId, message, messageHandle):
    action = ReqSendAction()
    action.ParseFromString(message.data)
    if 1 == action.actionType:
        set_amount_confirm_cmd.execute(userId, message, messageHandle)
