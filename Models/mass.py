from Models._element import _Element
from vector import Vector2D


class Mass(_Element):
    """
    Represents a mass inside a simulated, 2-D spacetime
    """

    def __init__(self, x: float, y: float, vx : float, vy : float, mass: float):
        """
        Constructs a Mass object
        :param x: the Masses x coordinate (kilometers)
        :param y: the Masses y coordinate (kilometers)
        :param vx : the x velocity of the mass
        :param vy: the y velocity of the mass
        :param mass: the mass of the Mass (kg)
        """
        super().__init__(x, y, vx, vy)
        self.__mass = mass

    @property
    def mass(self) -> float:
        """
        :return: The Mass's mass
        """
        return self.__mass
