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
        """
        Applies all the affects of gravity from the list of masses to this mass
        :param masses: the list of masses to calculate gravitational affects from
        :return: None
        """
        self.__total_gravitational_potential = 0
        for mass in masses:
            self._add_gravitational_potential(mass)

    def force_from(self, other : "Mass") -> float:
        """
        Calculate the gravitational force from the other mass on this mass
        :param other: the other mass to calculate force from.
        :return: None
        """
        return (SpaceTime.Gravitational_Constant * other.mass * self.mass) / self.distance_from(other)

    def _add_gravitational_potential(self, other : "Mass"):
        """
        Adds the gravitational potential from the provided mass to this mass's total potential.
        :param other: The other mass to calculate using.
        :return: None
        """
        self.__total_gravitational_potential += self.get_gravitational_potential(other)

    def get_gravitational_potential(self, other : "Mass") -> float:
        """
        Calculates the gravitational potential from the other mass that this mass is experiencing.
        :param other: The other mass in the calculation
        :return: the gravitational potential in units of Joules/kg
        """
        return -1 * ((SpaceTime.Gravitational_Constant * other.mass) / self.distance_from(other))

    @property
    def mass(self) -> float:
        """
        :return: The Mass's mass
        """
        return self.__mass
