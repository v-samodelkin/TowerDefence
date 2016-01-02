class HeartStone:
    defence = 1

    def __init__(self, X, Y, player):
        self.health = 500
        self.unpretty = 0
        self.X = X
        self.Y = Y
        self.player = player

    def Attack(self, damage):
        self.player.health -= damage
