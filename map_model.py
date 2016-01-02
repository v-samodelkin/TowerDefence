# -*- coding: utf8 -*-
import random
import itertools
from heapq import *
from MapObjects.Arrow import Arrow
from MapObjects.Cell import Cell
from MapObjects.Enemy import Enemy
from MapObjects.Ground import Ground
from MapObjects.HeartStone import HeartStone
from MapObjects.Player import Player
from MapObjects.Wall import Wall

switcher = {
    (0, -1): 2,
    (1, 0): 3,
    (0, 1): 0,
    (-1, 0): 1,
}


def Mid(x, y, z):
    return x <= y < z


def way(dx, dy):
    return switcher.get((dx, dy))


class MapModel:
    constdx = [0, 1, 0, -1]
    constdy = [1, 0, -1, 0]

    def playerX(self):
        for xy in itertools.product(range(self.width), range(self.height)):
            x = xy[0]
            y = xy[1]
            if (type(self.cells[x][y].obj) == Player):
                print("X " + str(x))
                return x

    def playerY(self):
        for xy in itertools.product(range(self.width), range(self.height)):
            x = xy[0]
            y = xy[1]
            if (type(self.cells[x][y].obj) == Player):
                print("Y " + str(y))
                return y

    def __init__(self, width, height, sizeOfCastle=8, playerPos=(3, 4), heartStonePos=(3, -3)):
        self.width = width
        self.height = height
        self.cells = []
        self.monsterWay = []
        self.whereToGo = []
        self.currentTurn = 0
        self.singletonGround = Ground()

        self.cells = [[Cell(self.singletonGround) for y in range(height)] for x in range(width)]
        self.monsterWay = [[1e9 for y in range(height)] for x in range(width)]
        self.whereToGo = [[[] for y in range(height)] for x in range(width)]

        cdx = self.constdx
        cdy = [-y for y in self.constdy]

        for xyk in itertools.product(range(width), range(height), range(4)):
            x = xyk[0]
            y = xyk[1]
            k = xyk[2]
            newX = x + cdx[k]
            newY = y + cdy[k]
            if (Mid(0, newX, self.width) and Mid(0, newY, self.height)):
                self.cells[x][y].ways[k].where = self.cells[newX][newY].ways[(k + 2) % 4]

        for i in range(sizeOfCastle):
            self.cells[i][-sizeOfCastle].SetObj(Wall(200) if random.randint(0, 5) > 3 else self.singletonGround)
            self.cells[sizeOfCastle - 1][-(i + 1)].SetObj(Wall(200) if random.randint(0, 5) > 3 else self.singletonGround)

        self.player = Player()
        self.cells[playerPos[0]][playerPos[1]].SetObj(self.player)
        self.heartstone = HeartStone((self.width + heartStonePos[0]) % self.width, (self.height + heartStonePos[1]) % self.height, self.player)
        self.cells[heartStonePos[0]][heartStonePos[1]].SetObj(self.heartstone)

    '''
    Передвигает игрока на заднное смещение, предварительно произведя ход
    '''
    def PlayerMove(self, dx, dy):
        px = self.playerX()
        py = self.playerY()
        if (Mid(0, px + dx, self.width) and Mid(0, py + dy, self.height)):
            self.Turn(dx, dy)

    def PlayerCorridorTurn(self, dx, dy):
        if (dx or dy):
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
                    arrow = Arrow(damage, self.constdx[i], self.constdy[i])
                    self.cells[newX][newY].ways[way(self.constdx[i], self.constdy[i])].SetObj(arrow)
        self.Turn()

    '''
    Обработка хода стрелы на клетке (x, y)
    '''
    def ArrowCorridorTurn(self, x, y):
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
    def EnemyCorridorTurn(self, x, y):
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
                    # Arrow
                    if ((type(self.cells[x][y].obj) == Arrow) and (turn <= Arrow.ExtraTurns)):
                        self.ArrowCorridorTurn(x, y)
                    # Enemy
                    elif ((type(self.cells[x][y].obj) == Enemy) and (turn <= Enemy.ExtraTurns)):
                        self.EnemyCorridorTurn(x, y)
                    # Player
                    elif ((type(self.cells[x][y].obj) == Player) and (turn <= Player.ExtraTurns)):
                        self.PlayerCorridorTurn(playerDX, playerDY)

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
                        if (self.cells[x][y].ways[i].obj is not None):
                            anybodyWaiting = True

                            cell = self.cells[x][y]
                            if (cell.ways[i].where.obj is not None):
                                objects = cell.ways[i].obj.Collision(cell.ways[i].where.obj)
                                if (objects[0] != None and objects[1] != None):
                                    objects[1], objects[0] = objects[0], objects[1]
                                cell.ways[i].SetObj(objects[1])
                                cell.ways[i].where.SetObj(objects[0])

                        if (self.cells[x][y].ways[i].obj is not None):
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
    def Turn(self, playerDX=0, playerDY=0):
        # Preload
        self.currentTurn += 1
        print("Turn: " + str(self.currentTurn))
        self.FindWay(self.heartstone.X, self.heartstone.Y)

        # Player
        self.player.DecreaseCooldown(1)

        # GenerateEnemies
        if (self.currentTurn % 4 == 0):
            self.GenerateEnemies(1)

        for turn in range(2):
            # Распихивание по комнатам ожидания
            self.InitWainingRooms(playerDX, playerDY, turn)

            # Обработка комнат ожидания
            self.DealWithWaitingRooms()

    def FindWay(self, X, Y):
        # Preload
        for i in range(self.width):
            for j in range(self.height):
                self.monsterWay[i][j] = 1e9
                self.whereToGo[i][j] = []
        self.monsterWay[X][Y] = 0
        visited = set()
        h = []
        heappush(h, (0, (X, Y)))

        # Start
        while h:
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
                    unpretty = self.cells[newX][newY].obj.unpretty
                    weight = current_weight + unpretty
                    if weight < self.monsterWay[newX][newY]:
                        self.monsterWay[newX][newY] = weight
                        heappush(h, (weight, (newX, newY)))
                        self.whereToGo[newX][newY] = []
                        self.whereToGo[newX][newY].append((curX, curY))
                    elif weight == self.monsterWay[newX][newY]:
                        self.whereToGo[newX][newY].append((curX, curY))
