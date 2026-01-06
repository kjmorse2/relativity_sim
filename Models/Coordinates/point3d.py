from __future__ import annotations
import math

from .point import Point


class Point3D(Point):
    """
    A point in 3D space stored internally in Cartesian coordinates (x, y, z).
    Provides computed spherical coordinate access.

    Use this class when Cartesian operations are primary.
    For spherical-primary storage, use SphericalPoint instead.
    """

    def __init__(self, x: float, y: float, z: float):
        """
        Initialize a Point3D from Cartesian coordinates.
        """
        self._x = x
        self._y = y
        self._z = z

    @classmethod
    def from_spherical(cls, r: float, theta: float, phi: float) -> "Point3D":
        """
        Create a Point3D from spherical coordinates.
        :param r: radial distance
        :param theta: polar angle (0 to π)
        :param phi: azimuthal angle (0 to 2π)
        """
        x = r * math.sin(theta) * math.cos(phi)
        y = r * math.sin(theta) * math.sin(phi)
        z = r * math.cos(theta)
        return cls(x, y, z)

    @staticmethod
    def _cartesian_to_spherical(x: float, y: float, z: float) -> tuple[float, float, float]:
        """Convert Cartesian (x, y, z) to spherical (r, theta, phi)."""
        r = math.sqrt(x**2 + y**2 + z**2)
        if r == 0:
            return 0.0, 0.0, 0.0
        theta = math.acos(z / r)  # polar angle
        phi = math.atan2(y, x)    # azimuthal angle
        return r, theta, phi

    # Cartesian coordinate properties (internal representation)
    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float):
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float):
        self._y = value

    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, value: float):
        self._z = value

    # Spherical coordinate properties (computed from Cartesian)
    @property
    def r(self) -> float:
        """Radial distance from origin."""
        return math.sqrt(self._x**2 + self._y**2 + self._z**2)

    @r.setter
    def r(self, value: float):
        current_r = self.r
        if current_r == 0:
            # If at origin, set position along z-axis
            self._z = max(0.0, value)
        else:
            # Scale position to new radius
            scale = max(0.0, value) / current_r
            self._x *= scale
            self._y *= scale
            self._z *= scale

    @property
    def theta(self) -> float:
        """Polar angle from positive z-axis (0 to π)."""
        r = self.r
        if r == 0:
            return 0.0
        return math.acos(self._z / r)

    @theta.setter
    def theta(self, value: float):
        r = self.r
        phi = self.phi
        # Normalize theta to [0, π]
        value = value % math.pi
        self._x = r * math.sin(value) * math.cos(phi)
        self._y = r * math.sin(value) * math.sin(phi)
        self._z = r * math.cos(value)

    @property
    def phi(self) -> float:
        """Azimuthal angle in x-y plane (0 to 2π)."""
        return math.atan2(self._y, self._x)

    @phi.setter
    def phi(self, value: float):
        r = self.r
        theta = self.theta
        # Normalize phi to [0, 2π)
        value = value % (2 * math.pi)
        self._x = r * math.sin(theta) * math.cos(value)
        self._y = r * math.sin(theta) * math.sin(value)
        self._z = r * math.cos(theta)

    def distance_to(self, other: "Point") -> float:
        """
        Calculate distance to another point using Cartesian coordinates.
        """
        dx = other.x - self._x
        dy = other.y - self._y
        dz = other.z - self._z
        return math.sqrt(dx**2 + dy**2 + dz**2)

    def direction_to(self, other: "Point") -> tuple[float, float]:
        """
        Calculate the angular direction (theta, phi) from this point toward another.
        Returns the angles representing the direction vector.
        """
        dx = other.x - self._x
        dy = other.y - self._y
        dz = other.z - self._z

        dist = math.sqrt(dx**2 + dy**2 + dz**2)
        if dist == 0:
            return 0.0, 0.0

        theta = math.acos(dz / dist)
        phi = math.atan2(dy, dx)
        return theta, phi

    def __repr__(self) -> str:
        return f"Point3D(x={self._x}, y={self._y}, z={self._z})"
