# -*- coding: utf8 -*-
from MapObjects.MapObject import MapObject


class Wall(MapObject):
    def __init__(self):
        super().__init__()
        self.health = 50
        self.unpretty = 80
        self.cost = 30

    def get_info(self):
        return "Спиральный генератор\nУрон: {0}\nПрочность: {1}".format(self.damage, self.health)

