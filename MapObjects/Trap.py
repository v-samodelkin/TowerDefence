from MapObjects.MapObject import MapObject


class Trap(MapObject):
    extra_turns = 0
    trap_colliders = {}

    def __init__(self):
        self.unpretty = 100