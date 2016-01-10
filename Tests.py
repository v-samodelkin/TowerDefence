import unittest
import MapModel
from itertools import product


class TextParserTests(unittest.TestCase):
    def test_steps(self):
        model = MapModel.MapModel(lambda: None, lambda: None, None)
        for _ in range(11):
            model.step()
        self.assertEqual(model.step_number, 1)

    def test_cooldown(self):
        model = MapModel.MapModel(lambda: None, lambda: None, None)
        model.player_fire(0)
        self.assertEqual(model.player.cooldown, 2)
        model.step()
        model.step()
        self.assertEqual(model.player.cooldown, 1)

    def test_way_search(self):
        model = MapModel.MapModel(lambda: None, lambda: None, None)
        model.find_way(0, 0)
        self.assertEqual(model.monster_way[1][2], MapModel.ground.unpretty * 3)

    def test_valid_of_default_map(self):
        model = MapModel.MapModel(lambda: None, lambda: None, None)
        heartstone_count = 0
        player_count = 0
        for (x, y) in product(range(MapModel.size), range(MapModel.size)):
            if isinstance(model.cells[x][y].obj, MapModel.Player):
                player_count += 1
            if isinstance(model.cells[x][y].obj, MapModel.HeartStone):
                heartstone_count += 1
        self.assertEqual(heartstone_count, 1)
        self.assertEqual(player_count, 1)

    def test_game_end(self):
        model = MapModel.MapModel(lambda: None, lambda: None, None)
        self.assertFalse(model.check_game_end())
        model.player.health = 0
        self.assertTrue(model.check_game_end())

    def test_player_kill(self):
        player = MapModel.Player()
        self.assertFalse(player.is_dead())
        player.collision(MapModel.Arrow(100500))
        self.assertTrue(player.is_dead())

    def test_no_suicide(self):
        model = MapModel.MapModel(lambda: None, lambda: None, None)
        for _ in range(150):
            model.step()
        self.assertEqual(0, model.get_killed_count())

    def test_no_immortality(self):
        spiral = MapModel.SpiralTower()
        for _ in range(1000):
            spiral.fired()
        self.assertIsNone(spiral.check())

    def test_no_cheating(self):
        spiral = MapModel.SpiralTower()
        health = spiral.health
        for _ in range(health):
            spiral.fired()
            spiral = spiral.check()
        self.assertIsNone(spiral)

    def test_annihilation(self):
        arrow1 = MapModel.Arrow(1)
        arrow2 = MapModel.Arrow(300)
        collide = arrow1.collision(arrow2)
        self.assertEqual(collide, (None, None))

    def test_destructible(self):
        wall = MapModel.Wall(400)
        arrow1 = MapModel.Arrow(300)
        arrow2 = MapModel.Arrow(90)
        arrow3 = MapModel.Arrow(10)
        self.assertEqual(wall.health, 400)
        arrow1.collision(wall)
        self.assertEqual(wall.health, 100)
        arrow2.collision(wall)
        arrow3.collision(wall)
        self.assertEqual(wall.health, 0)

if __name__ == "__main__":
    unittest.main()
