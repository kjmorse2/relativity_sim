from vector import Vector2D
from .mass import Mass

class SpaceTime:
    Gravitational_Constant : float = 6.67408e-11 # m^3 kg^-1 s^-2
    C : float = 299,792,458
    def __init__(self, size_x : float , size_y : float):
        self.__masses : list[Mass] = []
        self.__size_x : float = size_x
        self.__size_y : float = size_y
        self.__age : float = 0

    def add_mass(self, x: float, y: float, vx: float, vy: float, mass: float) -> Mass:
        velocity = Vector2D(x = vx, y = vy)
        mass = Mass(x, y, vx, vy, mass)
        self.__masses.append(mass)
        return mass

    def update(self, dt: float):
        for mass in self.__masses:
            mass.time_step(dt)

    @property
    def size_x(self) -> float:
        return self.__size_x

    @property
    def size_y(self) -> float:
        return self.__size_y

