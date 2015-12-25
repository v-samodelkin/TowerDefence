
class Controller:
    def __init__(self, viewer):
        self.viewer = viewer
        self.model = viewer.model

    def Start(self):
        self.viewer.view_map_model()
        self.viewer.top.bind("<Key>", self.Key)

    def key_to_moving(self, argument):
        switcher = {
            'w': (0, -1),
            's': (0, 1),
            'a': (-1, 0),
            'd': (1, 0),
        }
        return switcher.get(argument)

    def action_by_key(self, argument):
        switcher = {
            'w': (lambda:self.model.player_move(0,-1)),
            's': (lambda:self.model.player_move(0,1)),
            'a': (lambda:self.model.player_move(-1,0)),
            'd': (lambda:self.model.player_move(1,0)),
            'e': (lambda:self.model.Turn()),
            ' ': (lambda:self.model.player_fire(10)),
        }
        switcher.get(argument, lambda:None)()

    def Key(self, event):
        self.action_by_key(event.char)
        self.viewer.view_map_model()

