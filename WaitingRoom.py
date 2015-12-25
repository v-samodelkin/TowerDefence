import map_model as mm
class WaitingRoom:
    def __init__(self, obj, home):
        self.obj = obj;
        self.where = None
        self.home = home

    def SetObj(self, obj, hard = False):
        if (type(obj) == mm.Cell):
            print("AHTUNG!")
        self.obj = obj
        self.hard = hard