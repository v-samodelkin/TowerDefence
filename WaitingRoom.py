import map_model as mm
class WaitingRoom:
    def __init__(self, obj, home):
        self.obj = obj;
        self.where = None
        self.home = home

    def SetObj(self, obj, hard = False):
        assert not isinstance(obj, mm.Cell)
        self.obj = obj
        self.hard = hard