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
from MapObjects.Trap import Trap
from MapObjects.WalkableStructure import WalkableStructure
import Statistic as st


switcher = {
    (0, -1): 2,
    (1, 0): 3,
    (0, 1): 0,
    (-1, 0): 1,
}

singleton_ground = Ground()


def mid(x, y, z):
    return x <= y < z


def way(dx, dy):
    return switcher.get((dx, dy))


def not_on_game_end(func):
    def wrapper(map_model, *args, **kwargs):
        if not map_model.check_game_end():
            func(map_model, *args, **kwargs)
    return wrapper


class MapModel:
    constdx = [0, 1, 0, -1]
    constdy = [1, 0, -1, 0]

    def player_x(self):
        for (x, y) in itertools.product(range(self.width), range(self.height)):
            if isinstance(self.cells[x][y].obj, Player):
                return x

    def player_y(self):
        for (x, y) in itertools.product(range(self.width), range(self.height)):
            if isinstance(self.cells[x][y].obj, Player):
                return y

    def __init__(self, width, height, visualizer, on_game_over, castle_size=8, player_pos=(3, 4), heartstone_pos=(3, -3)):
        st.total_dead_enemies = 0
        self.width = width
        self.height = height
        self.cells = []
        self.monster_way = []
        self.where_to_go = []
        self.currentTurn = 0
        self.visualizer = visualizer
        self.on_game_over = on_game_over
        self.castle_size = castle_size
        self.player_pos = player_pos
        self.heartstone_pos = heartstone_pos
        self.step = 0

        self.cells = [[Cell(singleton_ground) for y in range(height)] for x in range(width)]
        self.monster_way = [[1e9 for y in range(height)] for x in range(width)]
        self.where_to_go = [[[] for y in range(height)] for x in range(width)]

        cdx = self.constdx
        cdy = [-y for y in self.constdy]

        for (x, y, k) in itertools.product(range(width), range(height), range(4)):
            new_x = x + cdx[k]
            new_y = y + cdy[k]
            if (mid(0, new_x, self.width) and mid(0, new_y, self.height)):
                self.cells[x][y].ways[k].where = self.cells[new_x][new_y].ways[(k + 2) % 4]

        for i in range(castle_size):
            self.cells[i][-castle_size].set_obj(Wall(200) if random.randint(0, 5) > 2 else singleton_ground)
            self.cells[castle_size - 1][-(i + 1)].set_obj(Wall(200) if random.randint(0, 5) > 2 else singleton_ground)

        self.player = Player()
        self.cells[player_pos[0]][player_pos[1]].set_obj(self.player)
        self.heartstone = HeartStone((self.width + heartstone_pos[0]) % self.width, (self.height + heartstone_pos[1]) % self.height, self.player)
        self.cells[heartstone_pos[0]][heartstone_pos[1]].set_obj(self.heartstone)

    def reset(self):
        self.__init__(self.width, self.height, self.visualizer,
                      self.on_game_over, self.castle_size, self.player_pos,
                      self.heartstone_pos)

    @not_on_game_end
    def player_move(self, dx, dy):
        '''
        Передвигает игрока на заднное смещение, предварительно произведя ход
        '''
        px = self.player_x()
        py = self.player_y()
        if (mid(0, px + dx, self.width) and mid(0, py + dy, self.height)):
            self.turn(dx, dy)

    def player_corridor_turn(self, dx, dy):
        if (dx or dy):
            px = self.player_x()
            py = self.player_y()
            if (mid(0, px + dx, self.width) and mid(0, py + dy, self.height)):
                self.cells[px + dx][py + dy].ways[way(dx, dy)].set_obj(self.player)
                self.cells[px][py].set_obj(self.cells[px][py].obj.get_from_below())

    @not_on_game_end
    def player_fire(self, damage):
        '''
        Производит выстрел в 4 стороны, затем производит ход
        '''
        if (self.player.cooldown == 0):
            self.player.fired()
            for i in range(4):
                newX = self.player_x() + self.constdx[i]
                newY = self.player_y() + self.constdy[i]
                if (mid(0, newX, self.width) and mid(0, newY, self.height)):
                    arrow = Arrow(damage, self.constdx[i], self.constdy[i])
                    self.cells[newX][newY].ways[way(self.constdx[i], self.constdy[i])].set_obj(arrow)
        self.turn()

    def ArrowCorridorTurn(self, x, y):
        '''
        Обработка хода стрелы на клетке (x, y)
        '''
        dx = self.cells[x][y].obj.dx
        dy = self.cells[x][y].obj.dy
        newx = dx + x
        newy = dy + y
        arrow = self.cells[x][y].obj
        self.cells[x][y].set_obj(self.cells[x][y].obj.get_from_below())
        arrow.from_below = None
        if (mid(0, newx, self.width) and mid(0, newy, self.height)):
            self.cells[newx][newy].ways[way(dx, dy)].set_obj(arrow)

    def EnemyCorridorTurn(self, x, y):
        '''
        Обработка хода врага на клетке (x, y)
        '''
        countOfWays = len(self.where_to_go[x][y])
        if countOfWays > 0:
            var = random.randint(0, countOfWays - 1)
            nx = self.where_to_go[x][y][var][0]
            ny = self.where_to_go[x][y][var][1]
            dx = nx - x
            dy = ny - y
            enemy = self.cells[x][y].obj
            self.cells[x][y].set_obj(self.cells[x][y].obj.get_from_below())
            enemy.from_below = None
            if (mid(0, nx, self.width) and mid(0, ny, self.height)):
                self.cells[nx][ny].ways[way(dx, dy)].set_obj(enemy)

    def InitWainingRooms(self, playerDX, playerDY, turn):
        '''
        Распихивание по комнатам ожидания
        '''
        for x in range(self.width):
            for y in range(self.height):
                    # Arrow
                    if ((type(self.cells[x][y].obj) == Arrow) and (turn in self.cells[x][y].obj.turns)):
                        self.ArrowCorridorTurn(x, y)
                    # Enemy
                    elif ((type(self.cells[x][y].obj) == Enemy) and (turn in self.cells[x][y].obj.turns)):
                        self.EnemyCorridorTurn(x, y)
                    # Player
                    elif ((type(self.cells[x][y].obj) == Player) and (turn in self.cells[x][y].obj.turns)):
                        self.player_corridor_turn(playerDX, playerDY)

    def generate_enemies(self, count):
        '''
        Генерация врагов
        '''
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
                self.cells[enemyX][enemyY].set_obj(Enemy(5, self.width, self.height))

    def deal_with_waiting_rooms(self):
        '''
        Обработка комнат ожидания
        '''
        anybody_waiting = True
        while anybody_waiting:
            anybody_waiting = False
            for x in range(self.width):
                for y in range(self.height):
                    for i in range(4):
                        if (self.cells[x][y].ways[i].obj is not None):
                            anybody_waiting = True

                            cell = self.cells[x][y]
                            if (cell.ways[i].where.obj is not None):
                                objects = cell.ways[i].obj.collision(cell.ways[i].where.obj)
                                if (objects[0] != None and objects[1] != None):
                                    objects[1], objects[0] = objects[0], objects[1]
                                cell.ways[i].set_obj(objects[1])
                                cell.ways[i].where.set_obj(objects[0])

                        if self.cells[x][y].ways[i].obj is not None:
                            anybody_waiting = True
                            cell = self.cells[x][y]
                            if (type(cell.obj) in cell.ways[i].obj.able_to_go):
                                objects = cell.ways[i].obj.collision(cell.obj)
                                if (objects[1] != None):
                                    cell.set_obj(objects[1])
                                else:
                                    cell.set_obj(singleton_ground)
                                if (objects[0] != None):
                                    cell.ways[i].where.set_obj(objects[0], True)
                                cell.ways[i].set_obj(None)
                            else:
                                cell.ways[i].obj, cell.ways[i].where.obj = None, cell.ways[i].obj

    @not_on_game_end
    def turn(self, player_dx=0, player_dy=0):
        '''
        Вычисление основных этапов хода
        '''
        if (self.step == 0):
            self.pre_turn()
        self.rooms_turn(player_dx, player_dy, self.step)
        self.step = (self.step + 1) % 6

    @not_on_game_end
    def player_place(self, what):
        '''
        Установка башни на клетку
        '''
        switcher = {
            1: self.place_trap,
            2: self.place_barrage,
            3: self.place_spiral,
        }
        switcher.get(what, lambda: None)()
        self.turn()

    def place_trap(self):
        if isinstance(self.player.from_below, Ground):
            trap = Trap(10, 15)
            if trap.cost <= st.player_gold:
                st.player_gold -= trap.cost
                self.player.from_below = trap

    def place_barrage(self):
        if isinstance(self.player.from_below, Ground):
            barrage = Wall(20)
            if barrage.cost <= st.player_gold:
                st.player_gold -= barrage.cost
                self.player.from_below = barrage

    def place_spiral(self):
        pass

    def pre_turn(self):
        '''
        Настройка перед серией из 6 тиков
        '''
        # Preload
        self.currentTurn += 1
        print("Turn: " + str(self.currentTurn))
        self.find_way(self.heartstone.x, self.heartstone.y)

        # Player
        self.player.decrease_cooldown(1)

        # GenerateEnemies
        if (self.currentTurn % 4 == 0):
            self.generate_enemies(1)

    def rooms_turn(self, player_dx, player_dy, turn):
        '''
        Один тик
        '''
        # Распихивание по комнатам ожидания
        self.InitWainingRooms(player_dx, player_dy, turn)

        # Обработка комнат ожидания
        self.deal_with_waiting_rooms()
        self.visualizer()

    def find_way(self, X, Y):
        '''
        Поиск пути до Камня жизни
        '''
        # Preload
        for i in range(self.width):
            for j in range(self.height):
                self.monster_way[i][j] = 1e9
                self.where_to_go[i][j] = []
        self.monster_way[X][Y] = 0
        visited = set()
        h = []
        heappush(h, (0, (X, Y)))

        # Start
        while h:
            min_node = heappop(h)
            curX = min_node[1][0]
            curY = min_node[1][1]
            if min_node[0] > self.monster_way[curX][curY]:
                continue
            if min_node is None:
                break
            visited.add(min_node[1])

            current_weight = self.monster_way[curX][curY]

            for i in range(4):
                newX = curX + self.constdx[i]
                newY = curY + self.constdy[i]
                if (mid(0, newX, self.width) and mid(0, newY, self.height)):
                    unpretty = self.cells[newX][newY].obj.unpretty
                    weight = current_weight + unpretty
                    if weight < self.monster_way[newX][newY]:
                        self.monster_way[newX][newY] = weight
                        heappush(h, (weight, (newX, newY)))
                        self.where_to_go[newX][newY] = []
                        self.where_to_go[newX][newY].append((curX, curY))
                    elif weight == self.monster_way[newX][newY]:
                        self.where_to_go[newX][newY].append((curX, curY))

    def check_game_end(self):
        '''
        Проверка на окончание игры
        '''
        if (self.player.is_dead()):
            self.on_game_over()
            return True
        return False
