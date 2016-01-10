# -*- coding: utf8 -*-
import MapModel as Mm
from MapObjects.MovingObject import MovingObject


class Player(MovingObject):
    def __init__(self):
        super().__init__()
        self.unpretty = 101
        self.cooldown = 0
        self.health = 30
        self.max_health = 30
        self.damage = 20
        self.able_to_go = {Mm.Arrow, Mm.Enemy, Mm.Ground, Mm.Trap}
        self.lazy_collision_init = self.collision_init

    def decrease_cooldown(self, count):
        self.cooldown -= count
        if self.cooldown < 0:
            self.cooldown = 0

    def get_info(self):
        return "Основной персонаж"

    def fired(self):
        self.cooldown = 3

    def check(self):
        return self

    def collision_init(self):
        @self.collide_registrar(Mm.Enemy)
        def enemy_collision(obj, enemy):
            obj.health -= enemy.damage * (enemy.health / obj.damage)
            if obj.health > 0:
                enemy.on_dead()
                return None, obj
            else:
                return None, enemy

        # noinspection PyUnusedLocal
        @self.collide_registrar(Mm.Ground)
        def ground_collision(obj, ground):
            return None, obj

        @self.collide_registrar(Mm.Arrow)
        def arrow_collision(obj, arrow):
            if obj.health > arrow.damage:
                obj.health -= arrow.damage
                return None, obj
            else:
                return None, None

        @self.collide_registrar(Mm.Trap)
        def walkable_structure_collide(obj, structure):
            obj.from_below = structure
            return None, obj
