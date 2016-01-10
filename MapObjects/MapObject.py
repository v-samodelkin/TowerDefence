class MapObject:
    def __init__(self):
        self.health = 1

    def get_info(self):
        return type(self).__name__

    def get_from_below(self):
        return self

    def check(self):
        return self if self.health > 0 else None
