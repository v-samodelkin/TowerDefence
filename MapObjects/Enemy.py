# -*- coding: utf8 -*-
import map_model as mm
import Statistic as st


class Enemy:
    extra_turns = 0
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    enemy_colliders = {}

    def __init__(self, health, width, height):
        self.able_to_go = {mm.Player, mm.Ground, mm.Arrow, mm.HeartStone}
        self.unpretty = 10000
        self.damage = 1
        self.health = health
        self.field = [[-1 for _ in range(height)] for _ in range(width)]
        self.lazy_collision_init = self.collision_init

    def collision(self, obj):
        self.lazy_collision_init()
        self.lazy_collision_init = lambda: None
        type1 = type(obj)
        try:
            return self.enemy_colliders[type1](self, obj)
        except KeyError:
            raise Exception('Enemy врезался в ' + str(type1))

    def on_dead(self):
        st.total_dead_enemies += 1

    def collide_registar(self, obstacle_class):
        def registered(func):
            self.enemy_colliders[obstacle_class] = func
            return func
        return registered

    def collision_init(self):
        @self.collide_registar(mm.Ground)
        def ground_collide(self, ground):
            return (None, self)

        @self.collide_registar(mm.HeartStone)
        def heartstone_collide(self, heartstone):
            heartstone.attack(self.damage * (self.health / heartstone.defence))
            return (None, heartstone)

        @self.collide_registar(mm.Arrow)
        def arrow_collide(self, arrow):
            if (self.health > arrow.damage):
                self.health -= arrow.damage
                return (None, self)
            else:
                self.on_dead()
                return (None, None)

        @self.collide_registar(mm.Player)
        def player_collide(self, player):
            player.health -= self.damage * (self.health / player.damage)
            if (player.health > 0):
                self.on_dead()
                return (None, player)
            else:
                return (None, self)
