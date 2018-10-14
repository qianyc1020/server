# coding=utf-8
class Game(object):
    alloc_id = None
    name = None
    uuid = None
    state = None

    def __init__(self, alloc_id, name, uuid):
        self.alloc_id = alloc_id
        self.name = name
        self.uuid = uuid
        self.state = 0
