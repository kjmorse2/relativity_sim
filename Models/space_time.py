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

    C : float = 299_792_458
    """
    The speed of light for this universe
    """
    def __init__(self):
        """
        Makes a new spacetime model
        """
        self.__masses : list[Mass] = []
        self.__age : float = 0

    def add_mass(self, x: float, y: float, z: float, vx: float, vy: float, vz: float, mass: float) -> Mass:
        """
        Adds a mass to this spacetime model.
        :param x: The x position of the mass.
        :param y: the y position of the mass.
        :param z: the z position of the mass.
        :param vx: the x velocity of the mass.
        :param vy: the y velocity of the mass.
        :param vz: the z velocity of the mass.
        :param mass: the mass (in kg) of the mass.
        :return: The Mass object created.
        """
        new_mass = Mass(x, y, z, vx, vy, vz, mass)
        self.__masses.append(new_mass)
        return new_mass

    def update(self, dt: float):
        """
        Updates the simulation by one time step.
        :param dt: The time step in seconds.
        """
        # Update all gravity related potentials/forces
        for i in range(0, len(self.__masses)):
            current_mass = self.__masses[i]
            other_masses = self.__masses.copy()
            other_masses.pop(i)
            current_mass.apply_gravity(other_masses)

        # Step forward in time
        for mass in self.__masses:
            mass.update_position(dt)

        self.__age += dt

    @property
    def masses(self) -> list[Mass]:
        """
        :return: The list of masses in this spacetime.
        """
        return self.__masses

    @property
    def age(self) -> float:
        """
        :return: The age of this spacetime in seconds.
        """
        return self.__age
