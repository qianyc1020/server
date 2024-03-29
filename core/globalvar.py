# coding=utf-8
import traceback


def init():
    global _global_dict
    _global_dict = {}


def set_v(name, value):
    _global_dict[name] = value


def get_v(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue


def del_v(name):
    try:
        del _global_dict[name]
    except:
        print traceback.print_exc()
