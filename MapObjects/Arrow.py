from MapObjects.Enemy import Enemy
from MapObjects.Ground import Ground
from MapObjects.Player import Player
from MapObjects.Wall import Wall
from MapObjects.HeartStone import HeartStone
import map_model as mm


class Arrow:
    ExtraTurns = 1
    ArrowColliders = {}

    def __init__(self, damage, dx, dy):
        self.damage = damage
        self.dx = dx
        self.dy = dy
        self.unpretty = 150
        self.ableToGo = {Player, Enemy, Wall, Ground, HeartStone}

    def Collision(self, obj):
        self.LazyCollisionInit()
        self.LazyCollisionInit = lambda: None
        type1 = type(obj)
        try:
            return self.ArrowColliders[type1](self, obj)
        except KeyError:
            raise Exception('Arrow hit in ' + str(type1))

    def CollideRegistrar(self, ObstacleClass):
        def Registered(func):
            self.ArrowColliders[ObstacleClass] = func
            return func
        return Registered

    def LazyCollisionInit(self):
        @self.CollideRegistrar(mm.Enemy)
        @self.CollideRegistrar(mm.Player)
        def AliveCollision(self, alive):
            revObjects = alive.Collision(self)
            return (revObjects[1], revObjects[0])

        @self.CollideRegistrar(mm.Wall)
        def WallCollision(self, wall):
            if (self.damage >= wall.health):
                return (None, None)
            else:
                wall.health -= self.damage
                return (None, wall)

        @self.CollideRegistrar(mm.Ground)
        def GroundCollision(self, ground):
            return (None, self)

        @self.CollideRegistrar(mm.HeartStone)
        def HeartStoneCollision(self, heartstone):
            return (None, heartstone)
