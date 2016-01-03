from ThreadForTimer import set_interval


class Controller:
    def __init__(self, viewer):
        self.viewer = viewer
        self.model = viewer.model
        self.stop = self.function()
        self.action = self.model.turn

    def start(self):
        self.viewer.view_map_model()
        self.viewer.top.bind("<Key>", self.key)

    def get_action_by_key(self, argument):
        switcher = {
            'w': (lambda: self.model.player_move(0, -1)),
            's': (lambda: self.model.player_move(0, 1)),
            'a': (lambda: self.model.player_move(-1, 0)),
            'd': (lambda: self.model.player_move(1, 0)),
            'e': (lambda: self.model.turn()),
            ' ': (lambda: self.model.player_fire(10)),
        }
        return switcher.get(argument, lambda: None)

    def key(self, event):
        self.action = self.get_action_by_key(event.char)
        self.viewer.view_map_model()

    @set_interval(.3)
    def function(self):
        self.action()
        self.viewer.view_map_model()
