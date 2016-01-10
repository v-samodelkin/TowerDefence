import MapModel as Mm
from MapObjects.Wall import Wall
from MapObjects.Player import Player
from MapObjects.HeartStone import HeartStone
import random
import itertools


def get_object_by_char(char, player):
    switcher = {
        '.': lambda: Mm.ground,
        'W': lambda: Wall(200),
        'P': lambda: player,
        '?': lambda: random_on_wall(),
        'S': lambda: Mm.SpiralTower(),
        'B': lambda: Wall(50),
        'T': lambda: Mm.Trap(10, 15),
        'H': lambda: HeartStone(player)
    }
    return switcher.get(char, lambda: Mm.ground)()


def random_on_wall():
    return Wall(200) if random.randint(0, 5) > 2 else Mm.ground


def get_default():
    castle_size = 8
    player_pos = (3, 4)
    heartstone_pos = (3, -3)
    height = width = Mm.size
    cells = [[Mm.ground for _ in range(height)] for _ in range(width)]
    for i in range(castle_size):
        cells[i][-castle_size] = random_on_wall()
        cells[castle_size - 1][-(i + 1)] = random_on_wall()

    player = Player()
    cells[player_pos[0]][player_pos[1]] = player
    heartstone = HeartStone(player)
    cells[heartstone_pos[0]][heartstone_pos[1]] = heartstone
    return cells


def read_from_file(filename):
    # noinspection PyBroadException
    try:
        with open(filename, "r") as f:
            height = width = 32
            lines = f.readlines()
            cells = [[Mm.ground for _ in range(height)] for _ in range(width)]
            player = Player()
            for (x, y) in itertools.product(range(width), range(height)):
                cells[x][y] = get_object_by_char(lines[y][x], player)
            return cells
    except Exception:
        return get_default()
