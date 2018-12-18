# coding=utf-8
class CreateGameDetails(object):

    def __init__(self, user_id, alloc_id, room_no, score, service_charge, time):
        self.user_id = user_id
        self.alloc_id = alloc_id
        self.room_no = room_no
        self.score = score
        self.service_charge = service_charge
        self.time = time
