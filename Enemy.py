# -*- coding: utf8 -*-
from queue import *
import map_model as mm
import Statistic as st
class Enemy:
    ExtraTurns = 0
    def __init__(self, health, width, height):
        self.ableToGo = {mm.Player, mm.Ground, mm.Arrow, mm.HeartStone}
        self.unpretty = 10000
        self.damage = 1
        self.health = health
        self.constdx = [0,1,0,-1]
        self.constdy = [1,0,-1,0]
        self.f = []
        for i in range(width):
            self.f.append([])
            for j in range(height):
                self.f[i].append(-1)

    def SearchWay(self, field, myX, myY, pX, pY):
        dX = 1 if myX < pX else 0 if myX == pX else -1
        dY = 1 if myY < pY else 0 if myY == pY else -1
        return (dX, dY)

    def SearchWay2(self, field, myX, myY):
        q = Queue()
        for i in range(field.width):
            for j in range(field.height):
                self.f[i][j] = -1
        q.put((myX, myY))
        while (not q.empty()):
            current = q.get()
            for i in range(4):
                newX = current[0] + self.constdx[i]
                newY = current[1] + self.constdy[i]
                if (mm.Mid(0, newX , field.width) and mm.Mid(0, newY, field.height)):
                    if (self.f[newX][newY] == -1):
                        q.put((newX, newY))
                        self.f[newX][newY] = self.f[current[0]][current[1]] + field.field[newX][newY].unpretty

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