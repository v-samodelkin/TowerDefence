import map_model as mm
from MapObjects.Cell import Cell
from MapObjects.Wall import Wall
from MapObjects.Player import Player
from MapObjects.HeartStone import HeartStone
import random


def get_default():
    castle_size=8
    player_pos=(3, 4)
    heartstone_pos=(3, -3)
    height = width =32
    cells = [[mm.singleton_ground for y in range(height)] for x in range(width)]
    for i in range(castle_size):
        cells[i][-castle_size] = (Wall(200) if random.randint(0, 5) > 2 else mm.singleton_ground)
        cells[castle_size - 1][-(i + 1)] = (Wall(200) if random.randint(0, 5) > 2 else mm.singleton_ground)

    player = Player()
    cells[player_pos[0]][player_pos[1]] = player
    heartstone = HeartStone((width + heartstone_pos[0]) % width, (height + heartstone_pos[1]) % height, player)

    cells[heartstone_pos[0]][heartstone_pos[1]] = heartstone

    return cells
