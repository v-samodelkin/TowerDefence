# -*- coding: utf8 -*-
import map_model as mm
import Statistic as st



class Enemy:
    ExtraTurns = 0
    Dx = [0,1,0,-1]
    Dy = [1,0,-1,0]
    EnemyColliders = {}

    def __init__(self, health, width, height):
        self.ableToGo = {mm.Player, mm.Ground, mm.Arrow, mm.HeartStone}
        self.unpretty = 10000
        self.damage = 1
        self.health = health
        self.field = [[-1 for _ in range(height)] for _ in range(width)]

    def Collision(self, obj):
        self.LazyCollisionInit()
        self.LazyCollisionInit = lambda: None
        type1 = type(obj)
        try:
            return self.EnemyColliders[type1](self, obj)
        except KeyError:
            raise Exception('Enemy врезался в ' + str(type1))


    def OnDead(self):
        st.TotalDeadEnem += 1


    def CollideRegistrar(self, ObstacleClass):
        def Registered(func):
            self.EnemyColliders[ObstacleClass] = func
            return func
        return Registered


    def LazyCollisionInit(self):
        @self.CollideRegistrar(mm.Ground)
        def GroundCollide(self, ground):
            return (None, self)

        @self.CollideRegistrar(mm.HeartStone)
        def HeartStoneCollide(self, heartstone):
            heartstone.Attack(self.damage * (self.health / heartstone.defence))
            return (None, heartstone)

        @self.CollideRegistrar(mm.Arrow)
        def ArrowCollide(self, arrow):
            if (self.health > arrow.damage):
                self.health -= arrow.damage
                return (None, self)
            else:
                self.OnDead()
                return (None, None)

        @self.CollideRegistrar(mm.Player)
        def PlayerCollide(self, player):
            player.health -= self.damage * (self.health / player.damage)
            if (player.health > 0):
                self.OnDead()
                return (None, player)
            else:
                return (None, self)