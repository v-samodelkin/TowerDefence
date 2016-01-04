# -*- coding: utf8 -*-
from MapObjects.MovingObject import MovingObject
import map_model as mm


class Arrow(MovingObject):
    def __init__(self, damage, dx, dy):
        super().__init__()
        self.turns = {2, 4}
        self.extra_turns = 1
        self.damage = damage
        self.dx = dx
        self.dy = dy
        self.unpretty = 150
        self.able_to_go = {mm.Player, mm.Enemy, mm.Wall, mm.Ground, mm.HeartStone}
        self.lazy_collision_init = self.collision_init

    def collision_init(self):
        @self.collide_registrar(mm.Enemy)
        @self.collide_registrar(mm.Player)
        def alive_collision(self, alive):
            rev_objects = alive.collision(self)
            return (rev_objects[1], rev_objects[0])

        @self.collide_registrar(mm.Wall)
        def wall_collision(self, wall):
            if (self.damage >= wall.health):
                return (None, None)
            else:
                wall.health -= self.damage
                return (None, wall)

        @self.collide_registrar(mm.Ground)
        def ground_collision(self, ground):
            return (None, self)

        @self.collide_registrar(mm.HeartStone)
        def heart_stone_collision(self, heartstone):
            return (None, heartstone)

    def get_info(self):
        return "Огненный шар\nУрон: {0}".format(self.damage)