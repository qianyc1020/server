# coding=utf-8
import time

def handler(msg):
    print("[Received: {0}] {1}".format(msg.subject, msg.data))