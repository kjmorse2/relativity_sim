import vector
from Models.point2d import Point2D

class _Element:
    def __init__(self, x: float, y: float, vx : float, vy : float):
        self.__position = Point2D(x, y)
        self.__velocity = vector.obj(x = vx, y = vy)
        self.__age = 0.0

    def update(self, dt: float):
        self.__position.x += self.__velocity.x * dt
        self.__position.y += self.__velocity.y * dt
        self.__age += dt

    @property
    def x(self) -> float:
        return self.__position.x

    @property
    def y(self) -> float:
        return self.__position.y

    @property
    def velocity(self) -> vector.VectorObject2D:
        return self.__velocity
    @property
    def age(self) -> float:
        return self.__age
