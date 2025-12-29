import vector
from Models.point2d import Point2D

class _Element:
    def __init__(self, x: float, y: float, vx : float, vy : float):
        """
        Initialize a Mass object.
        :param x: the initial x position
        :param y: the initial y position
        :param vx: the initial x velocity
        :param vy: the initial y velocity
        :param mass: the mass of the object
        """
        self.__position = Point2D(x, y)
        self.__velocity = vector.obj(x = vx, y = vy)
        self.__age = 0.0

    def time_step(self, dt: float):
        """
        Update the Mass's position based on its velocity and the time delta.
        :param dt: The amount of time passed
        :return: None
        """
        self.__position.x += self.__velocity.x * dt
        self.__position.y += self.__velocity.y * dt
        self.__age += dt
    def distance_from(self, other: "Mass") -> float:
        """
        Calculate the distance from this Mass to another Mass.
        :param other: The other Mass object
        :return: The distance between the two Mass objects
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx**2 + dy**2) ** 0.5

    @property
    def x(self) -> float:
        """
        :return: The Mass's x position
        """
        return self.__position.x

    @property
    def y(self) -> float:
        """
        :return: the Mass's y position
        """
        return self.__position.y

    @property
    def velocity(self) -> vector.VectorObject2D:
        """
        :return: The Mass's velocity
        """
        return self.__velocity

    @property
    def age(self) -> float:
        return self.__age
