# coding=utf-8
import ConfigParser


def init(path):
    global cf
    cf = ConfigParser.ConfigParser()
    cf.read(path)


def get(c, s):
    return cf.get(c, s)
