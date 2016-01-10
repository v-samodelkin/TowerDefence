# -*- coding: utf8 -*-
import random
from itertools import product
from heapq import *
from MapObjects.Arrow import Arrow
from MapObjects.Cell import Cell
from MapObjects.Enemy import Enemy
from MapObjects.Ground import Ground
from MapObjects.HeartStone import HeartStone
from MapObjects.Player import Player
from MapObjects.Wall import Wall
from MapObjects.Trap import Trap
from MapObjects.SpiralTower import SpiralTower
import Statistic
import MapParser
import TowerDefenceController as Tdc


direction_switcher = {
    (0, -1): 2,
    (1, 0): 3,
    (0, 1): 0,
    (-1, 0): 1,
}

ground = Ground()

size = 32


def mid(x, y, z):
    return x <= y < z


def way(dx, dy):
    return direction_switcher.get((dx, dy))


def not_on_game_end(func):
    def wrapper(map_model, *args, **kwargs):
        if not map_model.check_game_end():
            func(map_model, *args, **kwargs)
    return wrapper


class MapModel:
    constdx = [0, 1, 0, -1]
    constdy = [1, 0, -1, 0]

    def player_x(self):
        for (x, y) in product(range(size), range(size)):
            if isinstance(self.cells[x][y].obj, Player):
                return x

    def player_y(self):
        for (x, y) in product(range(size), range(size)):
            if isinstance(self.cells[x][y].obj, Player):
                return y

    def __init__(self, visualizer, on_game_over, map_name):
        Statistic.total_killed_enemies = 0
        Statistic.player_gold = 0
        self.end = False
        self.map_name = map_name
        self.cells = []
        self.monster_way = []
        self.where_to_go = []
        self.currentTurn = 0
        self.visualizer = visualizer
        self.on_game_over = on_game_over
        self.step_number = 0
        self.player = None
        self.cells = [[Cell(ground) for _ in range(size)] for _ in range(size)]
        self.monster_way = [[1e9 for _ in range(size)] for _ in range(size)]
        self.where_to_go = [[[] for _ in range(size)] for _ in range(size)]

        self.player_place_switcher = {
            1: self.place_trap,
            2: self.place_barrage,
            3: self.place_spiral,
        }

        cdx = self.constdx
        cdy = [-y for y in self.constdy]

        for (x, y, k) in product(range(size), range(size), range(4)):
            new_x = x + cdx[k]
            new_y = y + cdy[k]
            if mid(0, new_x, size) and mid(0, new_y, size):
                old_cell = self.cells[x][y]
                new_cell = self.cells[new_x][new_y]
                old_cell.ways[k].where = new_cell.ways[(k + 2) % 4]

        cells = MapParser.read_from_file(map_name)
        for (x, y) in product(range(size), range(size)):
            self.cells[x][y].set_obj(cells[x][y])
            if isinstance(cells[x][y], Player):
                self.player = cells[x][y]
            if isinstance(cells[x][y], HeartStone):
                self.heartstone = cells[x][y]
                self.heartstone_x = x
                self.heartstone_y = y

    def reset(self):
        self.__init__(self.visualizer, self.on_game_over, self.map_name)

    @not_on_game_end
    def player_move(self, dx, dy):
        """
        Передвигает игрока на заднное смещение, предварительно произведя ход
        """
        px = self.player_x()
        py = self.player_y()
        if mid(0, px + dx, size) and mid(0, py + dy, size):
            self.step(dx, dy)

    def player_corridor_turn(self, dx, dy):
        if dx or dy:
            px = self.player_x()
            py = self.player_y()
            if mid(0, px + dx, size) and mid(0, py + dy, size):
                new_cell = self.cells[px + dx][py + dy]
                new_cell.ways[way(dx, dy)].set_obj(self.player)
                old_cell = self.cells[px][py]
                old_cell.set_obj(self.cells[px][py].obj.get_from_below())

    def spiral_tower_turn(self, x, y):
        """
        Производит выстрел
        """
        tower = self.cells[x][y].obj
        tower.cooldown -= 1
        if tower.cooldown == 0:
            tower.fired()
            i = tower.direction
            newx = x + self.constdx[i]
            newy = y + self.constdy[i]
            if mid(0, newx, size) and mid(0, newy, size):
                arrow = Arrow(tower.damage, self.constdx[i], self.constdy[i])
                cell = self.cells[newx][newy]
                c_way = cell.ways[way(self.constdx[i], self.constdy[i])]
                c_way.set_obj(arrow)

    @not_on_game_end
    def player_fire(self, damage):
        """
        Производит выстрел в 4 стороны, затем производит ход
        """
        if self.player.cooldown == 0:
            self.player.fired()
            for i in range(4):
                newx = self.player_x() + self.constdx[i]
                newy = self.player_y() + self.constdy[i]
                if mid(0, newx, size) and mid(0, newy, size):
                    arrow = Arrow(damage, self.constdx[i], self.constdy[i])
                    cell = self.cells[newx][newy]
                    c_way = cell.ways[way(self.constdx[i], self.constdy[i])]
                    c_way.set_obj(arrow)
        self.step()

    def arrow_corridor_turn(self, x, y):
        """
        Обработка хода стрелы на клетке (x, y)
        """
        dx = self.cells[x][y].obj.get_dx()
        dy = self.cells[x][y].obj.get_dy()
        newx = dx + x
        newy = dy + y
        arrow = self.cells[x][y].obj
        self.cells[x][y].set_obj(self.cells[x][y].obj.get_from_below())
        arrow.from_below = None
        if mid(0, newx, size) and mid(0, newy, size):
            self.cells[newx][newy].ways[way(dx, dy)].set_obj(arrow)

    def enemy_corridor_turn(self, x, y):
        """
        Обработка хода врага на клетке (x, y)
        """
        count_of_ways = len(self.where_to_go[x][y])
        if count_of_ways > 0:
            var = random.randint(0, count_of_ways - 1)
            nx = self.where_to_go[x][y][var][0]
            ny = self.where_to_go[x][y][var][1]
            dx = nx - x
            dy = ny - y
            enemy = self.cells[x][y].obj
            self.cells[x][y].set_obj(self.cells[x][y].obj.get_from_below())
            enemy.from_below = None
            if mid(0, nx, size) and mid(0, ny, size):
                # noinspection PyTypeChecker
                self.cells[nx][ny].ways[way(dx, dy)].set_obj(enemy)

    def init_waiting_rooms(self, player_dx, player_dy, turn):
        """
        Распихивание по комнатам ожидания
        """
        for (x, y) in product(range(size), range(size)):
            obj = self.cells[x][y].obj
            # Arrow
            if isinstance(obj, Arrow) and (turn in obj.turns):
                self.arrow_corridor_turn(x, y)
            # Enemy
            elif isinstance(obj, Enemy) and (turn in obj.turns):
                self.enemy_corridor_turn(x, y)
            # Player
            elif isinstance(obj, Player) and (turn in obj.turns):
                self.player_corridor_turn(player_dx, player_dy)
            elif isinstance(obj, SpiralTower) and (turn in obj.turns):
                self.spiral_tower_turn(x, y)
                checked = self.cells[x][y].obj.check()
                self.cells[x][y].obj = checked if checked else ground

    def generate_enemies(self, count):
        """
        Генерация врагов
        """
        for cnt in range(count):
            enemy_x = random.randint(size - 3, size - 1)
            enemy_y = random.randint(0, 2)
            for i in range(10):
                if not isinstance(self.cells[enemy_x][enemy_y].obj, Ground):
                    enemy_x = random.randint(size - 3, size - 1)
                    enemy_y = random.randint(0, 2)
                else:
                    break
            if isinstance(self.cells[enemy_x][enemy_y].obj, Ground):
                self.cells[enemy_x][enemy_y].set_obj(Enemy(5, size, size))

    def deal_with_waiting_rooms(self):
        """
        Обработка комнат ожидания
        """
        anybody_waiting = True
        while anybody_waiting:
            anybody_waiting = False
            for (x, y, i) in product(range(size), range(size), range(4)):
                if self.cells[x][y].ways[i].obj is not None:
                    anybody_waiting = True

                    cell = self.cells[x][y]
                    if cell.ways[i].where.obj is not None:
                        c_way = cell.ways[i]
                        objects = c_way.obj.collision(cell.ways[i].where.obj)
                        if objects[0] is not None and objects[1] is not None:
                            objects[1], objects[0] = objects[0], objects[1]
                        c_way.set_obj(objects[1])
                        c_way.where.set_obj(objects[0])

                if self.cells[x][y].ways[i].obj is not None:
                    anybody_waiting = True
                    cell = self.cells[x][y]
                    obj = cell.ways[i].obj
                    if type(cell.obj) in obj.able_to_go:
                        objects = obj.collision(cell.obj)
                        if objects[1] is not None:
                            cell.set_obj(objects[1])
                        else:
                            cell.set_obj(ground)
                        if objects[0] is not None:
                            cell.ways[i].where.set_obj(objects[0], True)
                        cell.ways[i].set_obj(None)
                    else:
                        cell.ways[i].obj, cell.ways[i].where.obj = None, obj

    @not_on_game_end
    def step(self, player_dx=0, player_dy=0):
        """
        Вычисление основных этапов хода
        """
        if self.step_number == 0:
            self.pre_turn()
        self.rooms_turn(player_dx, player_dy, self.step_number)
        self.step_number = (self.step_number + 1) % 2

    @not_on_game_end
    def player_place(self, what):
        """
        Установка башни на клетку
        """
        self.player_place_switcher.get(what, lambda: None)()
        self.step()

    def place_trap(self):
        if isinstance(self.player.from_below, Ground):
            trap = Trap(10, 15)
            if trap.cost <= Statistic.player_gold:
                Statistic.player_gold -= trap.cost
                self.player.from_below = trap

    def place_barrage(self):
        if isinstance(self.player.from_below, Ground):
            barrage = Wall(20)
            if barrage.cost <= Statistic.player_gold:
                Statistic.player_gold -= barrage.cost
                self.player.from_below = barrage

    def place_spiral(self):
        if isinstance(self.player.from_below, Ground):
            spiral = SpiralTower()
            if spiral.cost <= Statistic.player_gold:
                Statistic.player_gold -= spiral.cost
                self.player.from_below = spiral

    def pre_turn(self):
        """
        Настройка перед серией из 6 тиков
        """
        # Preload
        self.currentTurn += 1
        self.find_way(self.heartstone_x, self.heartstone_y)

        # Player
        self.player.decrease_cooldown(1)

        # GenerateEnemies
        if self.currentTurn % 4 == 0:
            self.generate_enemies(1)

    def rooms_turn(self, player_dx, player_dy, turn):
        """
        Один тик
        """
        # Распихивание по комнатам ожидания
        self.init_waiting_rooms(player_dx, player_dy, turn)

        # Обработка комнат ожидания
        self.deal_with_waiting_rooms()
        self.visualizer()

    @staticmethod
    def get_killed_count():
        return Statistic.total_killed_enemies

    def find_way(self, x, y):
        """
        Поиск пути до Камня жизни
        """
        # Preload
        for (i, j) in product(range(size), range(size)):
            self.monster_way[i][j] = 1e9
            self.where_to_go[i][j] = []
        self.monster_way[x][y] = 0
        visited = set()
        h = []
        heappush(h, (0, (x, y)))

        # Start
        while h:
            min_node = heappop(h)
            cur_x = min_node[1][0]
            cur_y = min_node[1][1]
            if min_node[0] > self.monster_way[cur_x][cur_y]:
                continue
            if min_node is None:
                break
            visited.add(min_node[1])

            current_weight = self.monster_way[cur_x][cur_y]

            for i in range(4):
                newx = cur_x + self.constdx[i]
                newy = cur_y + self.constdy[i]
                if mid(0, newx, size) and mid(0, newy, size):
                    unpretty = self.cells[newx][newy].obj.unpretty
                    weight = current_weight + unpretty
                    if weight < self.monster_way[newx][newy]:
                        self.monster_way[newx][newy] = weight
                        heappush(h, (weight, (newx, newy)))
                        self.where_to_go[newx][newy] = []
                        self.where_to_go[newx][newy].append([cur_x, cur_y])
                    elif weight == self.monster_way[newx][newy]:
                        self.where_to_go[newx][newy].append([cur_x, cur_y])

    def check_game_end(self):
        """
        Проверка на окончание игры
        """
        if not self.player or self.player.is_dead():
            self.on_game_over()
            if not self.end:
                with open(Tdc.records_file_name, "a") as f:
                    f.write("{0}\n".format(Statistic.total_killed_enemies))
            self.end = True
            return True
        return False
