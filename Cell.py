from WaitingRoom import WaitingRoom
class Cell:
    def __init__(self, obj):
        self.obj = obj
        self.ways = []
        for i in range(4):
            self.ways.append(WaitingRoom(None, self))

    def SetObj(self, obj):
        self.obj = obj

