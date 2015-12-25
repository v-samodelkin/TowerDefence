# -*- coding: utf8 -*-
import random
from heapq import *
from Enemy import Enemy
from Cell import Cell
import Statistic as st
#statistic


def Mid(x, y, z):
    return ((x <= y) and (y < z))

def way(dx, dy):
    switcher = {
        (0, -1): 2,
        (1, 0): 3,
        (0, 1): 0,
        (-1, 0): 1,
    }
    return switcher.get((dx, dy))

class MapModel:
    def playerX(self):
        for x in range(self.width):
            for y in range(self.height):
                if (type(self.cells[x][y].obj) == Player):
                    print("X " + str(x))
                    return x
    def playerY(self):
        for x in range(self.width):
            for y in range(self.height):
                if (type(self.cells[x][y].obj) == Player):
                    print("Y " + str(y))
                    return y

    def __init__(self, width, height, sizeOfCastle = 8):
        self.width = width
        self.height = height
        self.cells = []
        self.monsterWay = []
        self.whereToGo = []
        self.currentTurn = 0
        self.singletonGround = Ground()
        self.constdx = [0,1,0,-1]
        self.constdy = [1,0,-1,0]


        for i in range(width):
            self.cells.append([])
            self.monsterWay.append([])
            self.whereToGo.append([])
            for j in range(height):
                self.cells[i].append(Cell(self.singletonGround))
                self.monsterWay[i].append(1e9)
                self.whereToGo[i].append([])
        cdx = [0,1,0,-1]
        cdy = [-1,0,1,0]
        for x in range(width):
            for y in range(height):
                for k in range(4):
                    newX = x + cdx[k]
                    newY = y + cdy[k]
                    if (Mid(0, newX, self.width) and Mid(0, newY, self.height)):
                        self.cells[x][y].ways[k].where = self.cells[newX][newY].ways[(k + 2) % 4]



        for i in range(0, sizeOfCastle):
            self.cells[i][height - sizeOfCastle].SetObj(Wall(200) if random.randint(0, 5) > 3 else self.singletonGround)
            self.cells[sizeOfCastle - 1][height - i - 1].SetObj(Wall(200) if random.randint(0, 5) > 3 else self.singletonGround)
        self.player = Player()
        self.cells[3][4].SetObj(self.player)
        self.heartstone = HeartStone(2, self.height - 3)
        self.cells[3][-3].SetObj(self.heartstone)


    '''
    Передвигает игрока на заднное смещение, предварительно произведя ход
    '''
    def player_move(self, dx, dy):
        px = self.playerX()
        py = self.playerY()
        if (Mid(0, px + dx, self.width) and Mid(0, py + dy, self.height)):
            self.Turn(dx, dy)


    def PlayerMove(self, dx, dy):
        if (dx != 0 or dy != 0):
            px = self.playerX()
            py = self.playerY()
            if (Mid(0, px + dx, self.width) and Mid(0, py + dy, self.height)):
                self.cells[px + dx][py + dy].ways[way(dx, dy)].SetObj(self.player)
                self.cells[px][py].SetObj(self.singletonGround)
    '''
    Производит выстрел в 4 стороны, затем производит ход
    '''
    def player_fire(self, damage):
        if (self.player.cooldown == 0):
            self.player.cooldown = 5
            for i in range(4):
                print("PlayerX: " + str(self.playerX()))
                newX = self.playerX() + self.constdx[i]
                newY = self.playerY() + self.constdy[i]
                if (Mid(0, newX, self.width) and Mid(0, newY, self.height)):
                    #if Arrow.AbleToGo(self.cells[newX][newY]):
                    arrow = Arrow(damage, self.constdx[i], self.constdy[i])
                    self.cells[newX][newY].ways[way(self.constdx[i], self.constdy[i])].SetObj(arrow)
            self.Turn()

    '''
    Обработка хода стрелы на клетке (x, y)
    '''
    def ArrowTurn(self, x, y):
        print("Arrow turn!")
        dx = self.cells[x][y].obj.dx
        dy = self.cells[x][y].obj.dy
        newx = dx + x
        newy = dy + y
        arrow = self.cells[x][y].obj
        if (Mid(0, newx, self.width) and Mid(0, newy, self.height)):
            self.cells[newx][newy].ways[way(dx, dy)].SetObj(arrow)
        self.cells[x][y].SetObj(self.singletonGround)
    '''
    Обработка хода врага на клетке (x, y)
    '''
    def EnemyTurn(self, x, y):
        countOfWays = len(self.whereToGo[x][y])
        if countOfWays > 0:
            var = random.randint(0, countOfWays - 1)
            newX = self.whereToGo[x][y][var][0]
            newY = self.whereToGo[x][y][var][1]
            dx = newX - x
            dy = newY - y
            enemy = self.cells[x][y].obj
            if (Mid(0, newX, self.width) and Mid(0, newY, self.height)):
                self.cells[newX][newY].ways[way(dx, dy)].SetObj(enemy)
        self.cells[x][y].SetObj(self.singletonGround)


    '''
    Распихивание по комнатам ожидания
    '''
    def InitWainingRooms(self, playerDX, playerDY, turn):
        for x in range(self.width):
            for y in range(self.height):
                    #Arrow
                    if ((type(self.cells[x][y].obj) == Arrow) and (turn <= Arrow.ExtraTurns)):
                        self.ArrowTurn(x, y)
                    #Enemy
                    elif ((type(self.cells[x][y].obj) == Enemy) and (turn <= Enemy.ExtraTurns)):
                        self.EnemyTurn(x, y)
                    #Player
                    elif ((type(self.cells[x][y].obj) == Player) and (turn <= Player.ExtraTurns)):
                        self.PlayerMove(playerDX, playerDY)

    '''
    Генерация врагов
    '''
    def GenerateEnemies(self, count):
        for cnt in range(count):
            enemyX = random.randint(self.width - 3, self.width - 1)
            enemyY = random.randint(0, 2)
            for i in range(10):
                if (type(self.cells[enemyX][enemyY].obj) != Ground):
                    enemyX = random.randint(self.width - 3, self.width - 1)
                    enemyY = random.randint(0, 2)
                else:
                    break
            if (type(self.cells[enemyX][enemyY].obj) == Ground):
                self.cells[enemyX][enemyY].SetObj(Enemy(5, self.width, self.height))

    '''
    Обработка комнат ожидания
    '''
    def DealWithWaitingRooms(self):
        anybodyWaiting = True
        while (anybodyWaiting):
            anybodyWaiting = False
            for x in range(self.width):
                for y in range(self.height):
                    for i in range(4):
                        if (self.cells[x][y].ways[i].obj != None):
                            anybodyWaiting = True

                            cell = self.cells[x][y]
                            if (cell.ways[i].where.obj != None):
                                objects = cell.ways[i].obj.Collision(cell.ways[i].where.obj)
                                if (objects[0] != None and objects[1] != None):
                                    objects[1], objects[0] = objects[0], objects[1]
                                cell.ways[i].SetObj(objects[1])
                                cell.ways[i].where.SetObj(objects[0])

                        if (self.cells[x][y].ways[i].obj != None):
                            anybodyWaiting = True
                            cell = self.cells[x][y]
                            if (type(cell.obj) in cell.ways[i].obj.ableToGo):
                                objects = cell.ways[i].obj.Collision(cell.obj)
                                if (objects[1] != None):
                                    cell.SetObj(objects[1])
                                else:
                                    cell.SetObj(self.singletonGround)
                                if (objects[0] != None):
                                    cell.ways[i].where.SetObj(objects[0], True)
                                cell.ways[i].SetObj(None)
                            else:
                                cell.ways[i].obj, cell.ways[i].where.obj = None, cell.ways[i].obj
    '''
    Вычисление основных этапов хода
    '''
    def Turn(self, playerDX = 0, playerDY = 0):
        #Preload
        self.currentTurn += 1
        print("Turn: " + str(self.currentTurn))
        self.FindWay(self.heartstone.X, self.heartstone.Y)

        #Player
        self.player.DecreaseCooldown(1)

        #GenerateEnemies
        if (self.currentTurn % 4 == 0):
            self.GenerateEnemies(1)

        for turn in range(2):
            #Распихивание по комнатам ожидания
            self.InitWainingRooms(playerDX, playerDY, turn)

            #Обработка комнат ожидания
            self.DealWithWaitingRooms()

    def FindWay(self, X, Y):
        #Preload
        for i in range(self.width):
            for j in range(self.height):
                self.monsterWay[i][j] = 1e9
                self.whereToGo[i][j] = []
        self.monsterWay[X][Y] = 0
        visited = set()
        h = []
        heappush(h, (0, (X, Y)))

        #Start
        while (len(h) != 0):
            min_node = heappop(h)
            curX = min_node[1][0]
            curY = min_node[1][1]
            if min_node[0] > self.monsterWay[curX][curY]:
                continue
            if min_node is None:
                break
            visited.add(min_node[1])


            current_weight = self.monsterWay[curX][curY]
            for i in range(4):
                newX = curX + self.constdx[i]
                newY = curY + self.constdy[i]
                if (Mid(0, newX, self.width) and Mid(0, newY, self.height)):
                    weight = current_weight + self.cells[newX][newY].obj.unpretty
                    if weight < self.monsterWay[newX][newY]:
                        self.monsterWay[newX][newY] = weight
                        heappush(h, (weight, (newX, newY)))
                        self.whereToGo[newX][newY] = []
                        self.whereToGo[newX][newY].append((curX, curY))
                    elif weight == self.monsterWay[newX][newY]:
                        self.whereToGo[newX][newY].append((curX, curY))


class Wall:
    def __init__(self, health):
        self.health = health
        self.unpretty = 1000

class Ground:
    def __init__(self):
        self.unpretty = 100



class Arrow:
    ExtraTurns = 1
    def __init__(self, damage, dx, dy):
        self.damage = damage
        self.dx = dx
        self.dy = dy
        self.unpretty = 150
        self.ableToGo = {Player, Enemy, Wall, Ground}

    def Collision(self, obj):
        type1 = type(obj)
        if ((type1 == Enemy) or (type1 == Player)):
            print("A -> E")
            revObjects = obj.Collision(self)
            return (revObjects[1], revObjects[0])
        elif (type1 == Wall):
            if (self.damage >= obj.health):
                return (None, None)
            else:
                obj.health -= self.damage
                return (None, obj)
        elif (type1 == Ground):
            return (None, self)
        raise Exception("Arrow врезалась в " + str(type1))


class HeartStone:
    def __init__(self, X, Y):
        self.health = 500
        self.unpretty = 0
        self.X = X
        self.Y = Y

class Player:
    ExtraTurns = 0
    def __init__(self):
        self.unpretty = 0
        self.cooldown = 0
        self.health = 30
        self.maxHealth = 30
        self.damage = 20
        self.ableToGo = {Arrow, Enemy, Ground}

    def AbleToGo(self, where):
        return (type(where) == Ground)

    def DecreaseCooldown(self, count):
        self.cooldown -= count
        if (self.cooldown < 0):
            self.cooldown = 0

    def Collision(self, obj):
        type1 = type(obj)
        if (type1 == Enemy):
            self.health -= obj.damage * (obj.health / self.damage)
            if (self.health > 0):
                print("Health:" + str(self.health))
                obj.OnDead()
                return (None, self)
            else:
                return (None, obj)
        elif (type1 == Wall):
            return (self, obj)
        elif (type1 == Ground):
            return (None, self)
        raise Exception("Player врезался в " + str(type1))