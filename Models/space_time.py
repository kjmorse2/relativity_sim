from .mass import Mass

class SpaceTime:
    """
    A model of spacetime
    Contains absolute parameters (speed of light, gravitational constant)
    """

    Gravitational_Constant : float = 6.67408e-11 # m^2 kg^-1 s^-2
    """
    The gravitational constat for this universe
    """
    C : float = 299,792,458
    """
    The speed of light for this universe
    """
    def __init__(self):
        """
        Makes a new spacetime model
        """
        self.__masses : list[Mass] = []
        self.__age : float = 0

    def add_mass(self, x: float, y: float, vx: float, vy: float, mass: float) -> Mass:
        """
        Adds a mass to this spacetime model.
        :param x: The x position of the mass.
        :param y: the y position of the mass.
        :param vx: the x velocity of the mass.
        :param vy: the y velocity of the mass.
        :param mass: the mass (in kg) of the mass.
        :return: The Mass object created.
        """
        mass = Mass(x, y, vx, vy, mass)
        self.__masses.append(mass)
        return mass

    def update(self, dt: float):
        for mass in self.__masses:
            mass.time_step(dt)