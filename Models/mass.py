from vector import Vector2D
from .space_time import SpaceTime
from ._element import _Element

class Mass(_Element):
    """
    Represents a mass inside a simulated, 2-D spacetime
    """

    def __init__(self, x: float, y: float, vx : float, vy : float, mass: float):
        """
        Constructs a Mass object
        :param mass: the mass of the Mass (kg)
        """
        super().__init__(x, y, vx, vy)
        self.__mass = mass
        self.__total_gravitational_potential = 0

    def apply_gravity(self, masses : list["Mass"]):
        self.__total_gravitational_potential = 0
        for mass in masses:
            self._add_gravitational_potential(mass)

    def _add_gravitational_potential(self, other : "Mass"):
        potential = -1 * ((SpaceTime.Gravitational_Constant * other.mass ) / self.distance_from(other))
        self.__total_gravitational_potential += potential

    @property
    def mass(self) -> float:
        """
        :return: The Mass's mass
        """
        return self.__mass
