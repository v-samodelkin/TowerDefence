# -*- coding: utf8 -*-
from MapObjects.MapObject import MapObject
from MapObjects.WalkableStructure import WalkableStructure


class Trap(MapObject, WalkableStructure):
    extra_turns = 0
    trap_colliders = {}

    def __init__(self, health, damage):
        super().__init__()
        self.cost = 40
        self.unpretty = 100
        self.health = health
        self.damage = damage

    def act_on_movable(self, movable):
        if self.health > 0:
            self.health -= 1
            movable.health -= self.damage

    def get_info(self):
        info = "Шипастая ловушка\n"
        info += "Урон: {0}".format(self.damage)
        info += "Прочность: {0}\n".format(self.health)
        return info
