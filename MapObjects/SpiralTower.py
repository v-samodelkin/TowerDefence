# -*- coding: utf8 -*-
from MapObjects.MapObject import MapObject


class SpiralTower(MapObject):
    def __init__(self):
        super().__init__()
        self.turns = {1}
        self.health = 200
        self.unpretty = 80
        self.cost = 30
        self.damage = 3
        self.cooldown = 10
        self.direction = 0

    def get_info(self):
        info = "Спиральный генератор\n"
        info += "Урон: {0}\n".format(self.damage)
        info += "Прочность: {0}\n".format(self.health)
        info += "Перезарядка: {0}".format(self.cooldown)
        return info

    def fired(self):
        self.cooldown = 1
        self.health -= 1
        self.direction = (self.direction + 1) % 4
