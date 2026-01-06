import unittest
import math
from Models.space_time import SpaceTime

class TestAbsFunction(unittest.TestCase):

    def setUp(self):
        self.SpaceTime = SpaceTime()

    def test_add_mass(self):
        """Test adding a mass with Cartesian input, verify position and spherical velocity."""
        mass = self.SpaceTime.add_mass(30, 40, 50, 2, 2, 2, 5)
        # Cartesian position should be preserved (computed from internal spherical)
        self.assertAlmostEqual(mass.x, 30, places=10)
        self.assertAlmostEqual(mass.y, 40, places=10)
        self.assertAlmostEqual(mass.z, 50, places=10)
        # Verify mass value
        self.assertEqual(mass.mass, 5)
        # Verify speed is correct (sqrt(2^2 + 2^2 + 2^2) = sqrt(12))
        expected_speed = math.sqrt(12)
        self.assertAlmostEqual(mass.speed, expected_speed, places=10)

    def test_spherical_position(self):
        """Test that position is correctly stored in spherical coordinates."""
        # Place mass at known spherical coordinates (r=10, theta=pi/4, phi=pi/4)
        r = 10.0
        theta = math.pi / 4
        phi = math.pi / 4
        x = r * math.sin(theta) * math.cos(phi)
        y = r * math.sin(theta) * math.sin(phi)
        z = r * math.cos(theta)

        mass = self.SpaceTime.add_mass(x, y, z, 0, 0, 0, 1)

        # Verify spherical coordinates
        self.assertAlmostEqual(mass.position.r, r, places=10)
        self.assertAlmostEqual(mass.position.theta, theta, places=10)
        self.assertAlmostEqual(mass.position.phi, phi, places=10)

    def test_update_mass_radial_velocity(self):
        """Test mass movement with purely radial velocity."""
        # Start at (10, 0, 0) with radial velocity pointing outward
        mass = self.SpaceTime.add_mass(10, 0, 0, 1, 0, 0, 10)
        initial_r = mass.position.r

        self.SpaceTime.update(3)

        # Mass should have moved radially outward
        # Position should have increased in r
        self.assertGreater(mass.position.r, initial_r)

if __name__ == "__main__":
    unittest.main()
