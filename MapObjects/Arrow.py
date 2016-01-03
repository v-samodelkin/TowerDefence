from MapObjects.Enemy import Enemy
from MapObjects.Ground import Ground
from MapObjects.Player import Player
from MapObjects.Wall import Wall
from MapObjects.HeartStone import HeartStone
import map_model as mm


class Arrow:
    extra_turns = 1
    arrow_colliders = {}

    def __init__(self, damage, dx, dy):
        self.damage = damage
        self.dx = dx
        self.dy = dy
        self.unpretty = 150
        self.able_to_go = {Player, Enemy, Wall, Ground, HeartStone}
        self.lazy_collision_init = self.collision_init

    def collision(self, obj):
        self.lazy_collision_init()
        self.lazy_collision_init = lambda: None
        type1 = type(obj)
        try:
            return self.arrow_colliders[type1](self, obj)
        except KeyError:
            raise Exception('Arrow hit in ' + str(type1))

    def collide_registar(self, obstacle_class):
        def registered(func):
            self.arrow_colliders[obstacle_class] = func
            return func
        return registered

    def collision_init(self):
        @self.collide_registar(mm.Enemy)
        @self.collide_registar(mm.Player)
        def alive_collision(self, alive):
            rev_objects = alive.collision(self)
            return (rev_objects[1], rev_objects[0])

        @self.collide_registar(mm.Wall)
        def wall_collision(self, wall):
            if (self.damage >= wall.health):
                return (None, None)
            else:
                wall.health -= self.damage
                return (None, wall)

        @self.collide_registar(mm.Ground)
        def ground_collision(self, ground):
            return (None, self)

        @self.collide_registar(mm.HeartStone)
        def heart_stone_collision(self, heartstone):
            return (None, heartstone)
