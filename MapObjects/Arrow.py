# -*- coding: utf8 -*-
from MapObjects.MovingObject import MovingObject
import MapModel as Mm


class Arrow(MovingObject):
    def __init__(self, damage, dx, dy):
        super().__init__()
        self.turns = {0, 1}
        self.extra_turns = 1
        self.damage = damage
        self.dx = dx
        self.dy = dy
        self.unpretty = 150
        self.able_to_go = {Mm.Player, Mm.Enemy, Mm.Wall,
                           Mm.Ground, Mm.HeartStone, Mm.Trap,
                           Mm.Arrow, Mm.SpiralTower}
        self.lazy_collision_init = self.collision_init

    def get_dx(self):
        return self.dx

    def get_dy(self):
        return self.dy

    def collision_init(self):
        @self.collide_registrar(Mm.Enemy)
        @self.collide_registrar(Mm.Player)
        def alive_collision(obj, alive):
            alive.health -= obj.damage
            if alive.health > 0:
                return None, alive
            else:
                alive.on_dead()
                return None, alive.get_from_below()

        @self.collide_registrar(Mm.Wall)
        def wall_collision(obj, wall):
            wall.health -= obj.damage
            if wall.health <= 0:
                return None, None
            else:
                return None, wall

        # noinspection PyUnusedLocal
        @self.collide_registrar(Mm.Ground)
        def ground_collision(obj, ground):
            return None, obj

        # noinspection PyUnusedLocal
        @self.collide_registrar(Mm.HeartStone)
        def heart_stone_collision(obj, heartstone):
            return None, heartstone

        @self.collide_registrar(Mm.Trap)
        def walkable_structure_collide(obj, structure):
            self.from_below = structure
            return None, obj

        # noinspection PyUnusedLocal
        @self.collide_registrar(Mm.Arrow)
        def arrow_collide(obj, arrow):
            return None, None

        # noinspection PyUnusedLocal
        @self.collide_registrar(Mm.SpiralTower)
        def spiral_collide(obj, spiral):
            return None, spiral

    def get_info(self):
        return "Энергетический шар\nУрон: {0}".format(self.damage)
