# -*- coding: utf8 -*-
import map_model as mm
from MapObjects.MovingObject import MovingObject
import Statistic as st


class Enemy(MovingObject):
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]

    def __init__(self, health, width, height):
        super().__init__()
        self.able_to_go = {mm.Player, mm.Ground, mm.Arrow, mm.HeartStone}
        self.unpretty = 10000
        self.damage = 1
        self.health = health
        self.field = [[-1 for _ in range(height)] for _ in range(width)]
        self.lazy_collision_init = self.collision_init

    def on_dead(self):
        st.total_dead_enemies += 1
        return self.get_from_below()

    def get_info(self):
        return "Панда\nЗдоровье: {0}\nУрон: {1}".format(self.health, self.damage)

    def collision_init(self):
        @self.collide_registrar(mm.Ground)
        def ground_collide(self, ground):
            return (None, self)

        @self.collide_registrar(mm.HeartStone)
        def heartstone_collide(self, heartstone):
            heartstone.attack(self.damage * (self.health / heartstone.defence))
            return (None, heartstone)

        @self.collide_registrar(mm.Arrow)
        def arrow_collide(self, arrow):
            self.health -= arrow.damage
            if (self.health > 0):
                return (None, self)
            else:
                self.on_dead()
                return (None, None)

        @self.collide_registrar(mm.Player)
        def player_collide(self, player):
            player.health -= self.damage * (self.health / player.damage)
            self.health -= player.damage * (self.health / player.damage)
            if (player.health > 0):
                self.on_dead()
                return (None, player)
            else:
                return (None, self)

