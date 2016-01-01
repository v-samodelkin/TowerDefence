
class Controller:
    def __init__(self, viewer):
        self.viewer = viewer
        self.model = viewer.model

    def Start(self):
        self.viewer.view_map_model()
        self.viewer.top.bind("<Key>", self.Key)

    def ActionByKey(self, argument):
        switcher = {
            'w': (lambda:self.model.PlayerMove(0,-1)),
            's': (lambda:self.model.PlayerMove(0,1)),
            'a': (lambda:self.model.PlayerMove(-1,0)),
            'd': (lambda:self.model.PlayerMove(1,0)),
            'e': (lambda:self.model.Turn()),
            ' ': (lambda:self.model.player_fire(10)),
        }
        switcher.get(argument, lambda:None)()

    def Key(self, event):
        self.ActionByKey(event.char)
        self.viewer.view_map_model()

