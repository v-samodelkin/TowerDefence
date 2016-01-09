from ThreadForTimer import set_interval


class Controller:



    def __init__(self, viewer, init):
        self.viewer = viewer
        self.model = viewer.model
        self.stop = self.function()
        self.action = self.model.turn
        self.get_action = {
            'w': (lambda: self.model.player_move(0, -1)),
            's': (lambda: self.model.player_move(0, 1)),
            'a': (lambda: self.model.player_move(-1, 0)),
            'd': (lambda: self.model.player_move(1, 0)),
            'e': (lambda: self.model.turn()),
            ' ': (lambda: self.model.player_fire(10)),
            '1': (lambda: self.model.player_place(1)),
            '2': (lambda: self.model.player_place(2)),
            '3': (lambda: self.model.player_place(3)),
        }
        self.do_action = {
            'r': (lambda: self.try_restart()),
        }

    def callback(self, event):
        x = event.x // self.viewer.size_of_element
        y = event.y // self.viewer.size_of_element
        self.viewer.show_info_about_cell(x, y)

    def start(self):
        self.viewer.view_map_model()
        self.viewer.top.bind("<Key>", self.key)
        self.viewer.top.bind("<Button-1>", self.callback)

    def get_action_by_key(self, argument):
        return self.get_action.get(argument, lambda: None)

    def do_action_by_key(self, argument):
        self.do_action.get(argument, lambda: None)()

    def try_restart(self):
        if self.model.check_game_end():
            self.viewer.before_restart()
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

    @set_interval(.02)
    def function(self):
        self.action()
        if self.model.check_game_end():
            self.stop.set()
