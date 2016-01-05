from ThreadForTimer import set_interval


class Controller:
    def __init__(self, viewer, init):
        self.viewer = viewer
        self.model = viewer.model
        self.stop = self.function()
        self.action = self.model.turn
        self.aa = 0

    def callback(self, event):
        x = event.x // self.viewer.size_of_element
        y = event.y // self.viewer.size_of_element
        self.viewer.show_info_about_cell(x, y)

    def start(self):
        self.viewer.view_map_model()
        self.viewer.top.bind("<Key>", self.key)
        self.viewer.top.bind("<Button-1>", self.callback)


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

    def do_action_by_key(self, argument):
        switcher = {
            'r': (lambda: self.try_restart()),
        }
        switcher.get(argument, lambda: None)()

    def try_restart(self):
        ge = self.model.check_game_end()
        print(ge)
        if ge:
            self.stop.set()
            self.stop.clear()
            self.viewer.view_map_model(hard=True)
            self.stop = self.function()
            self.viewer.model.reset()
            self.action = self.model.turn


    def key(self, event):
        self.action = self.get_action_by_key(event.char)
        self.do_action_by_key(event.char)
        self.viewer.view_map_model()


    @set_interval(.01)
    def function(self):
        self.action()
        self.aa += 1
        if self.model.check_game_end():
            self.stop.set()
