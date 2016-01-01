from MapObjects.Enemy import Enemy
from MapObjects.Ground import Ground
from MapObjects.Wall import Wall
class Player:
    ExtraTurns = 0
    def __init__(self):
        from MapObjects.Arrow import Arrow
        self.unpretty = 0
        self.cooldown = 0
        self.health = 30
        self.maxHealth = 30
        self.damage = 20
        self.ableToGo = {Arrow, Enemy, Ground}

    def AbleToGo(self, where):
        return (type(where) == Ground)

    def DecreaseCooldown(self, count):
        self.cooldown -= count
        if (self.cooldown < 0):
            self.cooldown = 0

    def Collision(self, obj):
        if (isinstance(obj, Enemy)):
            self.health -= obj.damage * (obj.health / self.damage)
            if (self.health > 0):
                print("Health:" + str(self.health))
                obj.OnDead()
                return (None, self)
            else:
                return (None, obj)
        elif (isinstance(obj, Wall)):
            return (self, obj)
        elif (isinstance(obj, Ground)):
            return (None, self)
        raise Exception("Player hit in " + str(type(obj)))


