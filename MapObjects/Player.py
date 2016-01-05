# -*- coding: utf8 -*-
import map_model as mm
from MapObjects.MovingObject import MovingObject
class Player(MovingObject):
    def __init__(self):
        super().__init__()
        self.unpretty = 200
        self.cooldown = 0
        self.health = 30
        self.max_health = 30
        self.damage = 20
        self.able_to_go = {mm.Arrow, mm.Enemy, mm.Ground}
        self.lazy_collision_init = self.collision_init

    def decrease_cooldown(self, count):
        self.cooldown -= count
        if (self.cooldown < 0):
            self.cooldown = 0

    def get_info(self):
        return "Основной персонаж"

    def fired(self):
        self.cooldown = 3

    def collision_init(self):
        @self.collide_registrar(mm.Enemy)
        def enemy_Collision(self, enemy):
            self.health -= enemy.damage * (enemy.health / self.damage)
            if (self.health > 0):
                enemy.on_dead()
                return (None, self)
            else:
                return (None, enemy)

        @self.collide_registrar(mm.Ground)
        def ground_Collision(self, ground):
            return (None, self)

        @self.collide_registrar(mm.Arrow)
        def arrow_collision(self, arrow):
            if (self.health > arrow.damage):
                self.health -= arrow.damage
                return (None, self)
            else:
                return (None, None)