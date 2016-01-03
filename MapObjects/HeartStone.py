class HeartStone:
    defence = 1

    def __init__(self, x, y, player):
        self.health = 500
        self.unpretty = 0
        self.x = x
        self.y = y
        self.player = player

    def attack(self, damage):
        self.player.health -= damage
