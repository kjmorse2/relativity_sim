from Models._element import _Element
from vector import Vector2D

class Particle(_Element):
    def __init__(self, x: float, y: float, vx : float, vy : float):
        super().__init__(x, y, vx, vy)
        self.__age = 0

    def update(self, dt: float):
        super().update(dt)
        self.__age += dt
