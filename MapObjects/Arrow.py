from MapObjects.Enemy import Enemy
from MapObjects.Ground import Ground
from MapObjects.Player import Player
from MapObjects.Wall import Wall


class Arrow:
    ExtraTurns = 1

    def __init__(self, damage, dx, dy):
        self.damage = damage
        self.dx = dx
        self.dy = dy
        self.unpretty = 150
        self.ableToGo = {Player, Enemy, Wall, Ground}

    def Collision(self, obj):
        if (isinstance(obj, Enemy) or isinstance(obj, Player)):
            print("A -> E")
            revObjects = obj.Collision(self)
            return (revObjects[1], revObjects[0])
        elif (isinstance(obj, Wall)):
            if (self.damage >= obj.health):
                return (None, None)
            else:
                obj.health -= self.damage
                return (None, obj)
        elif (isinstance(obj, Ground)):
            return (None, self)
        raise Exception("Arrow hit in " + str(type(obj)))
