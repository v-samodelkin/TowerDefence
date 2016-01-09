# -*- coding: utf8 -*-
from MapObjects.MapObject import MapObject


class Wall(MapObject):
    def __init__(self, health):
        super().__init__()
        self.max_health = health
        self.health = health
        self.unpretty = 1000
        self.cost = health // 2

    def get_info(self):
        return "Стена \nПрочность: {0}".format(self.health)
