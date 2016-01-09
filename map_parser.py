import map_model as mm
from MapObjects.Cell import Cell
from MapObjects.Wall import Wall
from MapObjects.Player import Player
from MapObjects.HeartStone import HeartStone
import random
import itertools


def get_object_by_char(char, player, x, y):
    switcher = {
        '.': lambda: mm.singleton_ground,
        'W': lambda: Wall(200),
        'P': lambda: player,
        '?': lambda: random_on_wall(),
        'S': lambda: mm.SpiralTower(),
        'B': lambda: Wall(50),
        'T': lambda: mm.Trap(10, 15),
        'H': lambda: HeartStone(x, y, player)
    }
    return switcher.get(char, lambda: mm.singleton_ground)()

def random_on_wall():
    return Wall(200) if random.randint(0, 5) > 2 else mm.singleton_ground

def get_default():
    castle_size=8
    player_pos=(3, 4)
    heartstone_pos=(3, -3)
    height = width = 32
    cells = [[mm.singleton_ground for y in range(height)] for x in range(width)]
    for i in range(castle_size):
        cells[i][-castle_size] = random_on_wall()
        cells[castle_size - 1][-(i + 1)] = random_on_wall()

    player = Player()
    cells[player_pos[0]][player_pos[1]] = player
    heartstone = HeartStone((width + heartstone_pos[0]) % width, (height + heartstone_pos[1]) % height, player)
    cells[heartstone_pos[0]][heartstone_pos[1]] = heartstone
    return cells

def read_from_file(filename):
    try:
        with open(filename, "r") as f:
            height = width = 32
            lines = f.readlines()
            cells = [[mm.singleton_ground for y in range(height)] for x in range(width)]
            player = Player()
            for (x, y) in itertools.product(range(width), range(height)):
                cells[x][y] = get_object_by_char(lines[y][x], player, x, y)
            return cells
    except:
        return get_default()