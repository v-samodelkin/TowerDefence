# -*- coding: utf8 -*-
import MapModel as Mm
from MapObjects.MovingObject import MovingObject
import Statistic


class Enemy(MovingObject):
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]

    def __init__(self, health, width, height):
        super().__init__()
        self.gold = 2
        self.able_to_go = {Mm.Player, Mm.Ground, Mm.Arrow,
                           Mm.HeartStone, Mm.Trap, Mm.Wall, Mm.SpiralTower}
        self.unpretty = 10000
        self.damage = 1
        self.health = health
        self.field = [[-1 for _ in range(height)] for _ in range(width)]
        self.lazy_collision_init = self.collision_init

    def on_dead(self):
        Statistic.total_killed_enemies += 1
        Statistic.player_gold += self.gold
        return self.get_from_below()

    def get_info(self):
        info = "Панда\n"
        info += "Здоровье: {0}\n".format(self.health)
        info += "Урон: {0}\n".format(self.damage)
        return info

    def collision_init(self):
        # noinspection PyUnusedLocal
        @self.collide_registrar(Mm.Ground)
        def ground_collide(obj, ground):
            return None, obj

        @self.collide_registrar(Mm.HeartStone)
        def heartstone_collide(obj, heartstone):
            heartstone.attack(obj.damage * (obj.health / heartstone.defence))
            return None, heartstone

        @self.collide_registrar(Mm.Arrow)
        def arrow_collide(obj, arrow):
            obj.health -= arrow.damage
            if self.health > 0:
                return None, obj
            else:
                self.on_dead()
                return None, obj.get_from_below()

        @self.collide_registrar(Mm.Player)
        def player_collide(obj, player):
            player.health -= obj.damage * (obj.health / player.damage)
            obj.health -= player.damage * (obj.health / player.damage)
            if player.health > 0:
                obj.on_dead()
                return None, player
            else:
                return None, obj

        @self.collide_registrar(Mm.Trap)
        def trap_collide(obj, structure):
            structure.act_on_movable(obj)
            if obj.health > 0:
                obj.from_below = structure
                return None, obj
            else:
                obj.on_dead()
                return None, structure.check()

        @self.collide_registrar(Mm.SpiralTower)
        @self.collide_registrar(Mm.Wall)
        def wall_collide(obj, wall):
            damage = obj.damage * obj.health
            if damage > wall.health:
                obj.health -= wall.health / obj.damage
                return None, obj
            else:
                wall.health -= damage
                return None, wall.check()
