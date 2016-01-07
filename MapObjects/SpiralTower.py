# -*- coding: utf8 -*-
from MapObjects.MapObject import MapObject


class SpiralTower(MapObject):
    def __init__(self):
        super().__init__()
        self.turns = {5}
        self.health = 200
        self.unpretty = 80
        self.cost = 30
        self.damage = 3
        self.cooldown = 10
        self.direction = 0

    def get_info(self):
        return "Спиральный генератор\nУрон: {0}\nПрочность: {1}\nПерезарядка: {2}".format(self.damage, self.health, self.cooldown)

    def fired(self):
        self.cooldown = 1
        self.health -= 1
        self.direction = (self.direction + 1) % 4