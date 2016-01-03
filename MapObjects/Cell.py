from WaitingRoom import WaitingRoom


class Cell:
    def __init__(self, obj):
        self.obj = obj
        self.ways = [WaitingRoom(None, self) for x in range(4)]

    def set_obj(self, obj):
        self.obj = obj
