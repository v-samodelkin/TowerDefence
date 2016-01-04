# -*- coding: utf8 -*-
from MapObjects.MapObject import MapObject


class Ground(MapObject):
    def __init__(self):
        self.unpretty = 100

    def get_info(self):
        return "Кусок земли \nНичего интересного"