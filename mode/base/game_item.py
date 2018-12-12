# coding=utf-8
class Game(object):

    def __init__(self, alloc_id, name, uuid):
        self.alloc_id = alloc_id
        self.name = name
        self.uuid = uuid
        self.state = 0
