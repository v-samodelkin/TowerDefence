# -*- coding: utf8 -*-
from MapObjects.MovingObject import MovingObject
import map_model as mm


class Arrow(MovingObject):
    def __init__(self, damage, dx, dy):
        super().__init__()
        self.turns = {2, 5}
        self.extra_turns = 1
        self.damage = damage
        self.dx = dx
        self.dy = dy
        self.unpretty = 150
        self.able_to_go = {mm.Player, mm.Enemy, mm.Wall, mm.Ground, mm.HeartStone, mm.Trap, mm.Arrow, mm.SpiralTower}
        self.lazy_collision_init = self.collision_init

    def get_dx(self):
        return self.dx

    def get_dy(self):
        return self.dy


    def collision_init(self):
        @self.collide_registrar(mm.Enemy)
        @self.collide_registrar(mm.Player)
        def alive_collision(self, alive):
            alive.health -= self.damage
            if (alive.health > 0):
                return (None, alive)
            else:
                alive.on_dead()
                return (None, alive.get_from_below())

        @self.collide_registrar(mm.Wall)
        def wall_collision(self, wall):
            wall.health -= self.damage
            if (wall.health <= 0):
                return (None, None)
            else:
                return (None, wall)

        @self.collide_registrar(mm.Ground)
        def ground_collision(self, ground):
            return (None, self)

        @self.collide_registrar(mm.HeartStone)
        def heart_stone_collision(self, heartstone):
            return (None, heartstone)

        @self.collide_registrar(mm.Trap)
        def walkable_structure_collide(self, structure):
            self.from_below = structure
            return (None, self)

        @self.collide_registrar(mm.Arrow)
        def arrow_collide(self, arrow):
            return None, None

        @self.collide_registrar(mm.SpiralTower)
        def spiral_collide(self, spiral):
            return None, spiral

    def get_info(self):
        return "Энергетический шар\nУрон: {0}".format(self.damage)
