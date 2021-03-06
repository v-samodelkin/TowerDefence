import MapModel as Mm


class WaitingRoom:
    def __init__(self, obj, home):
        self.obj = obj
        self.where = None
        self.home = home
        self.hard = False

    def set_obj(self, obj, hard=False):
        assert not isinstance(obj, Mm.Cell)
        self.obj = obj
        self.hard = hard
