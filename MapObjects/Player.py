import map_model as mm
class Player:
    extra_turns = 0
    player_colliders = {}
    def __init__(self):
        self.unpretty = 0
        self.cooldown = 0
        self.health = 30
        self.max_health = 30
        self.damage = 20
        self.able_to_go = {mm.Arrow, mm.Enemy, mm.Ground}
        self.lazy_collision_init = self.collision_init

    def decrease_cooldown(self, count):
        self.cooldown -= count
        if (self.cooldown < 0):
            self.cooldown = 0

    def collision(self, obj):
        self.lazy_collision_init()
        self.lazy_collision_init = lambda: None
        type1 = type(obj)
        try:
            return self.player_colliders[type1](self, obj)
        except KeyError:
            raise Exception('Player hit in ' + str(type1))

    def collide_registrar(self, obstacle_class):
        def registered(func):
            self.player_colliders[obstacle_class] = func
            return func
        return registered


    def collision_init(self):
        @self.collide_registrar(mm.Enemy)
        def enemy_Collision(self, enemy):
            self.health -= enemy.damage * (enemy.health / self.damage)
            if (self.health > 0):
                enemy.on_dead()
                return (None, self)
            else:
                return (None, enemy)

        @self.collide_registrar(mm.Ground)
        def ground_Collision(self, ground):
            return (None, self)

        @self.collide_registrar(mm.Arrow)
        def arrow_collision(self, arrow):
            if (self.health > arrow.damage):
                self.health -= arrow.damage
                return (None, self)
            else:
                return (None, None)