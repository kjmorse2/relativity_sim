from __future__ import annotations

from Coordinates.spherical_point import SphericalPoint
from Coordinates.spherical_velocity import SphericalVelocity


class _Element:
    def __init__(self, x: float, y: float, z: float, vx: float, vy: float, vz: float):
        """
        Initialize an Element object from Cartesian coordinates.
        Internally stores position and velocity in spherical coordinates.
        :param x: the initial x position (Cartesian)
        :param y: the initial y position (Cartesian)
        :param z: the initial z position (Cartesian)
        :param vx: the initial x velocity (Cartesian)
        :param vy: the initial y velocity (Cartesian)
        :param vz: the initial z velocity (Cartesian)
        """
        self.position = SphericalPoint(x, y, z)
        self._velocity = SphericalVelocity.from_cartesian(vx, vy, vz, self.position)
        self._age = 0.0

    def time_step(self, dt: float):
        """
        Update the Element's position based on its velocity and the time delta.
        Uses spherical coordinate dynamics.
        :param dt: The amount of time passed
        :return: None
        """
        # Update spherical coordinates directly
        self.position.r += self._velocity.v_r * dt
        self.position.theta += self._velocity.v_theta * dt
        self.position.phi += self._velocity.v_phi * dt
        self._age += dt

    def distance_from(self, other: "_Element") -> float:
        """
        Calculate the distance from this Element to another Element.
        Uses spherical coordinate distance formula.
        :param other: The other Element object
        :return: The distance between the two Element objects
        """
        return self.position.distance_to(other.position)

    @property
    def x(self) -> float:
        """
        :return: The Element's x position (Cartesian)
        """
        return self.position.x

    @property
    def y(self) -> float:
        """
        :return: The Element's y position (Cartesian)
        """
        return self.position.y

    @property
    def z(self) -> float:
        """
        :return: The Element's z position (Cartesian)
        """
        return self.position.z

    @property
    def velocity(self) -> SphericalVelocity:
        """
        :return: The Element's velocity in spherical coordinates
        """
        return self._velocity

    @velocity.setter
    def velocity(self, value: SphericalVelocity):
        """
        Set the Element's velocity
        :param value: The new velocity (SphericalVelocity)
        """
        self._velocity = value

    @property
    def speed(self) -> float:
        """
        :return: The Element's speed (magnitude of velocity)
        """
        return self._velocity.magnitude(self.position)

    @property
    def age(self) -> float:
        return self._age
