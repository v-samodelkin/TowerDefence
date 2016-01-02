import map_model as mm
class Player:
    ExtraTurns = 0
    PlayerColliders = {}
    def __init__(self):
        self.unpretty = 0
        self.cooldown = 0
        self.health = 30
        self.maxHealth = 30
        self.damage = 20
        self.ableToGo = {mm.Arrow, mm.Enemy, mm.Ground}

    def AbleToGo(self, where):
        return (type(where) == mm.Ground)

    def DecreaseCooldown(self, count):
        self.cooldown -= count
        if (self.cooldown < 0):
            self.cooldown = 0

    def Collision(self, obj):
        self.LazyCollisionInit()
        self.LazyCollisionInit = lambda: None
        type1 = type(obj)
        try:
            return self.PlayerColliders[type1](self, obj)
        except KeyError:
            raise Exception('Player hit in ' + str(type1))

    def CollideRegistrar(self, ObstacleClass):
        def Registered(func):
            self.PlayerColliders[ObstacleClass] = func
            return func
        return Registered


    def LazyCollisionInit(self):
        @self.CollideRegistrar(mm.Enemy)
        def EnemyCollision(self, enemy):
            self.health -= enemy.damage * (enemy.health / self.damage)
            if (self.health > 0):
                enemy.OnDead()
                return (None, self)
            else:
                return (None, enemy)

        @self.CollideRegistrar(mm.Ground)
        def GroundCollision(self, ground):
            return (None, self)

        @self.CollideRegistrar(mm.Arrow)
        def ArrowCollision(self, arrow):
            if (self.health > arrow.damage):
                self.health -= arrow.damage
                return (None, self)
            else:
                return (None, None)