from Models.particle import Particle
from Models.mass import Mass
from vector import Vector2D

class SpaceTime:
    def __init__(self, size_x : float , size_y : float):
        self.__particles : list[Particle] = []
        self.__masses : list[Mass] = []
        self.__size_x : float = size_x
        self.__size_y : float = size_y
        self.__age : float = 0

    def add_point(self, x: float, y: float, vx: float, vy: float) -> Particle:
        velocity = Vector2D(x = vx, y = vy)
        particle = Particle(x, y, vx, vy)
        self.__particles.append(particle)
        return particle

    def add_mass(self, x: float, y: float, vx: float, vy: float, mass: float) -> Mass:
        velocity = Vector2D(x = vx, y = vy)
        mass = Mass(x, y, vx, vy, mass)
        self.__masses.append(mass)
        return mass

    def update(self, dt: float):
        for particle in self.__particles:
            particle.update(dt)
        for mass in self.__masses:
            mass.update(dt)

    def get_particles(self) -> list[Particle]:
        return self.__particles

    @property
    def size_x(self) -> int:
        return self.__size_x

    @property
    def size_y(self) -> int:
        return self.__size_y

