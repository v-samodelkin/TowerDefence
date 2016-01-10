# -*- coding: utf8 -*-
from MapObjects.MapObject import MapObject


class HeartStone(MapObject):
    defence = 1

    def __init__(self, player):
        super().__init__()
        self.health = 500
        self.unpretty = 0
        self.player = player

    def attack(self, damage):
        self.player.health -= damage

    def get_info(self):
        return "Амулет жизни"
