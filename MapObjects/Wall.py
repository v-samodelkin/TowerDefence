# -*- coding: utf8 -*-
from MapObjects.MapObject import MapObject
from MapObjects.WalkableStructure import WalkableStructure


class Wall(MapObject):
    def __init__(self, health):
        super().__init__()
        self.health = health
        self.unpretty = 1000

    def get_info(self):
        return "Стена \nПрочность: {0}".format(self.health)

