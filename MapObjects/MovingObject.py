import map_model as mm
from MapObjects.MapObject import MapObject


class MovingObject(MapObject):
    def __init__(self):
        self.gold = 0
        self.turns = {3}
        self.extra_turns = 0
        self.unpretty = 100
        self.colliders = {}
        self.able_to_go = {mm.Ground}
        self.damage = 1
        self.health = 1
        self.lazy_collision_init = self.collision_init
        self.from_below = None

    def collision(self, obj):
        self.lazy_collision_init()
        self.lazy_collision_init = lambda: None
        type1 = type(obj)
        try:
            return self.colliders[type1](self, obj)
        except KeyError:
            raise Exception(str(type(self)) + ' hit in ' + str(type1))

    def collide_registrar(self, obstacle_class):
        def registered(func):
            self.colliders[obstacle_class] = func
            return func
        return registered

    def collision_init(self):
        @self.collide_registrar(mm.Ground)
        def ground_Collision(self, ground):
            return (None, self)

    def on_dead(self):
        return mm.singleton_ground

    def get_from_below(self):
        return self.from_below

    def is_dead(self):
        return self.health <= 0
