import unittest
from Models.space_time import SpaceTime

class TestAbsFunction(unittest.TestCase):

    def setUp(self):
        self.SpaceTime = SpaceTime(100, 100)

    def test_add_point(self):
        particle = self.SpaceTime.add_point(10, 20, 1, 1)
        self.assertEqual(particle.x, 10)
        self.assertEqual(particle.y, 20)
        self.assertEqual(particle.velocity.x, 1)
        self.assertEqual(particle.velocity.y, 1)

    def test_update_particle(self):
        particle = self.SpaceTime.add_point(0, 0, 1, 1)
        self.SpaceTime.update(5)
        self.assertEqual(particle.x, 5)
        self.assertEqual(particle.y, 5)

    def test_add_mass(self):
        mass = self.SpaceTime.add_mass(30, 40, 2, 2, 5)
        self.assertEqual(mass.x, 30)
        self.assertEqual(mass.y, 40)
        self.assertEqual(mass.velocity.x, 2)
        self.assertEqual(mass.velocity.y, 2)
        self.assertEqual(mass.mass, 5)

    def test_update_mass(self):
        mass = self.SpaceTime.add_mass(0, 0, 2, 2, 10)
        self.SpaceTime.update(3)
        self.assertEqual(mass.x, 6)
        self.assertEqual(mass.y, 6)

if __name__ == "__main__":
    unittest.main()
