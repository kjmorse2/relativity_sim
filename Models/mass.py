from __future__ import annotations
from typing import TYPE_CHECKING
import math

from ._element import _Element
from .spherical_velocity import SphericalVelocity
from .spherical_force import SphericalForce

if TYPE_CHECKING:
    from .space_time import SpaceTime


class Mass(_Element):
    """
    Represents a mass inside a simulated, 3-D spacetime.
    Uses spherical coordinates internally for physics calculations,
    which is ideal for gravitational simulations and Schwarzschild metric.
    """

    def __init__(self, x: float, y: float, z: float, vx: float, vy: float, vz: float, mass: float):
        """
        Constructs a Mass object from Cartesian coordinates.
        :param x: the initial x position (Cartesian)
        :param y: the initial y position (Cartesian)
        :param z: the initial z position (Cartesian)
        :param vx: the initial x velocity (Cartesian)
        :param vy: the initial y velocity (Cartesian)
        :param vz: the initial z velocity (Cartesian)
        :param mass: the mass of the Mass (kg)
        """
        super().__init__(x, y, z, vx, vy, vz)
        self._mass = mass
        self._total_gravitational_potential = 0.0
        self._net_force = SphericalForce()

    def apply_gravity(self, masses: list["Mass"]):
        """
        Applies all the effects of gravity from the list of masses to this mass.
        Calculates force in spherical coordinates where gravity is naturally radial.
        :param masses: the list of masses to calculate gravitational effects from
        :return: None
        """
        self._net_force.reset()
        self._total_gravitational_potential = 0.0

        for other_mass in masses:
            self._add_gravitational_potential(other_mass)
            force = self.force_from(other_mass)
            self._net_force = self._net_force + force

    def force_from(self, other: "Mass") -> SphericalForce:
        """
        Calculate the gravitational force from the other mass on this mass.
        Returns force in spherical coordinates relative to this mass's position.

        For gravity, the force is purely radial (pointing toward the other mass),
        which is a natural representation in spherical coordinates.

        :param other: the other mass to calculate force from.
        :return: SphericalForce representing the gravitational attraction
        """
        from .space_time import SpaceTime

        distance = self.distance_from(other)
        if distance == 0:
            return SphericalForce()

        # Gravitational force magnitude (always attractive, toward other mass)
        magnitude = (SpaceTime.Gravitational_Constant * other.mass * self.mass) / (distance ** 2)

        # Calculate direction angles from this mass to the other mass
        # These angles define the direction of the force in spherical coordinates
        theta_dir, phi_dir = self.position.direction_to(other.position)

        # Decompose the force into spherical components at this mass's position
        # The force points from this mass toward the other mass
        sin_theta_dir = math.sin(theta_dir)
        cos_theta_dir = math.cos(theta_dir)
        sin_phi_dir = math.sin(phi_dir)
        cos_phi_dir = math.cos(phi_dir)

        # Transform force direction to spherical components relative to this position
        sin_theta_pos = math.sin(self.position.theta)
        cos_theta_pos = math.cos(self.position.theta)
        sin_phi_pos = math.sin(self.position.phi)
        cos_phi_pos = math.cos(self.position.phi)

        # Unit vector in direction of other mass (Cartesian)
        ux = sin_theta_dir * cos_phi_dir
        uy = sin_theta_dir * sin_phi_dir
        uz = cos_theta_dir

        # Project onto spherical basis vectors at this position
        # e_r = (sin(theta)cos(phi), sin(theta)sin(phi), cos(theta))
        # e_theta = (cos(theta)cos(phi), cos(theta)sin(phi), -sin(theta))
        # e_phi = (-sin(phi), cos(phi), 0)

        F_r = magnitude * (ux * sin_theta_pos * cos_phi_pos +
                          uy * sin_theta_pos * sin_phi_pos +
                          uz * cos_theta_pos)

        F_theta = magnitude * (ux * cos_theta_pos * cos_phi_pos +
                              uy * cos_theta_pos * sin_phi_pos -
                              uz * sin_theta_pos)

        F_phi = magnitude * (-ux * sin_phi_pos + uy * cos_phi_pos)

        return SphericalForce(F_r, F_theta, F_phi)

    def _add_gravitational_potential(self, other: "Mass"):
        """
        Adds the gravitational potential from the provided mass to this mass's total potential.
        Gravitational potential is a scalar, so coordinate system doesn't matter.
        :param other: The other mass to calculate using.
        :return: None
        """
        self._total_gravitational_potential += self.get_gravitational_potential(other)

    def get_gravitational_potential(self, other: "Mass") -> float:
        """
        Calculates the gravitational potential from the other mass that this mass is experiencing.
        :param other: The other mass in the calculation
        :return: the gravitational potential in units of Joules/kg
        """
        distance = self.distance_from(other)
        if distance == 0:
            return 0.0
        return -1 * ((SpaceTime.Gravitational_Constant * other.mass) / distance)

    def update_position(self, dt: float):
        """
        Update position based on current velocity and forces.
        All calculations done in spherical coordinates.
        :param dt: time step in seconds
        """
        r = self.position.r
        sin_theta = math.sin(self.position.theta)

        # Calculate acceleration in spherical coordinates
        # a = F / m
        a_r = self._net_force.F_r / self._mass
        a_theta = self._net_force.F_theta / (self._mass * r)
        a_phi = self._net_force.F_phi / (self._mass * r * sin_theta)

        # Update velocity components
        delta_v = SphericalVelocity(a_r * dt, a_theta * dt, a_phi * dt)
        self.velocity = self.velocity + delta_v

        # Update position using spherical kinematics
        self.position.r += self.velocity.v_r * dt
        self.position.theta += self.velocity.v_theta * dt
        self.position.phi += self.velocity.v_phi * dt

    def relative_time(self, absolute_dt: float) -> float:
        """
        Calculates the relative time experienced at this point in space.
        Placeholder for Schwarzschild time dilation calculation.
        :param absolute_dt: The absolute time passed in the universe
        :return: the relative time experienced at this point.
        """

        return absolute_dt

    @property
    def mass(self) -> float:
        """
        :return: The Mass's mass
        """
        return self._mass

    @property
    def net_force(self) -> SphericalForce:
        """
        :return: The net force on this mass in spherical coordinates
        """
        return self._net_force

    @property
    def gravitational_potential(self) -> float:
        """
        :return: The total gravitational potential at this mass's position
        """
        return self._total_gravitational_potential
