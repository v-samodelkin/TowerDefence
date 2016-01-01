# -*- coding: utf8 -*-
import map_model as mm
import Statistic as st
class Enemy:
    ExtraTurns = 0
    Dx = [0,1,0,-1]
    Dy = [1,0,-1,0]

    def __init__(self, health, width, height):
        self.ableToGo = {mm.Player, mm.Ground, mm.Arrow, mm.HeartStone}
        self.unpretty = 10000
        self.damage = 1
        self.health = health
        self.field = [[-1 for _ in range(height)] for _ in range(width)]

    def Collision(self, obj):
        type1 = type(obj)
        if (type1 == mm.Arrow):
            print("E -> A")
            if (self.health > obj.damage):
                print("Alive!")
                self.health -= obj.damage
                return (None, self)
            else:
                self.OnDead()
                return (None, None)
        elif (type1 == mm.Player):
            obj.health -= self.damage * (self.health / obj.damage)
            if (obj.health > 0):
                print("Health(e):" + str(obj.health))
                self.OnDead()
                return (None, obj)
            else:
                return (None, self)
        elif (type1 == mm.Ground):
            return (None, self)
        elif (type1 == mm.HeartStone):
            return (None, self)
        raise Exception('Enemy врезался в ' + str(type1))

    def OnDead(self):
        st.TotalDeadEnem += 1