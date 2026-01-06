from __future__ import annotations
import math

from .point import Point


class SphericalPoint(Point):
    """
    A point in 3D space stored internally in spherical coordinates (r, theta, phi).
    - r: radial distance from origin
    - theta: polar angle from positive z-axis (0 to π)
    - phi: azimuthal angle in x-y plane from positive x-axis (0 to 2π)

    This is the primary point class optimized for gravitational simulations
    and Schwarzschild metric calculations.
    """

    def __init__(self, x: float, y: float, z: float):
        """
        Initialize a SphericalPoint from Cartesian coordinates.
        Internally converts to and stores spherical coordinates.
        """
        self._r, self._theta, self._phi = self._cartesian_to_spherical(x, y, z)

    @classmethod
    def from_spherical(cls, r: float, theta: float, phi: float) -> "SphericalPoint":
        """
        Create a SphericalPoint directly from spherical coordinates.
        :param r: radial distance
        :param theta: polar angle (0 to π)
        :param phi: azimuthal angle (0 to 2π)
        """
        instance = cls.__new__(cls)
        instance._r = r
        instance._theta = theta
        instance._phi = phi
        return instance

    @staticmethod
    def _cartesian_to_spherical(x: float, y: float, z: float) -> tuple[float, float, float]:
        """Convert Cartesian (x, y, z) to spherical (r, theta, phi)."""
        r = math.sqrt(x**2 + y**2 + z**2)
        if r == 0:
            return 0.0, 0.0, 0.0
        theta = math.acos(z / r)  # polar angle
        phi = math.atan2(y, x)    # azimuthal angle
        return r, theta, phi

    @staticmethod
    def _spherical_to_cartesian(r: float, theta: float, phi: float) -> tuple[float, float, float]:
        """Convert spherical (r, theta, phi) to Cartesian (x, y, z)."""
        x = r * math.sin(theta) * math.cos(phi)
        y = r * math.sin(theta) * math.sin(phi)
        z = r * math.cos(theta)
        return x, y, z

    # Spherical coordinate properties (internal representation)
    @property
    def r(self) -> float:
        """Radial distance from origin."""
        return self._r

    @r.setter
    def r(self, value: float):
        self._r = max(0.0, value)  # r cannot be negative

    @property
    def theta(self) -> float:
        """Polar angle from positive z-axis (0 to π)."""
        return self._theta

    @theta.setter
    def theta(self, value: float):
        # Normalize theta to [0, π]
        self._theta = value % math.pi

    @property
    def phi(self) -> float:
        """Azimuthal angle in x-y plane (0 to 2π)."""
        return self._phi

    @phi.setter
    def phi(self, value: float):
        # Normalize phi to [0, 2π)
        self._phi = value % (2 * math.pi)

    # Cartesian coordinate properties (computed from spherical)
    @property
    def x(self) -> float:
        x, _, _ = self._spherical_to_cartesian(self._r, self._theta, self._phi)
        return x

    @x.setter
    def x(self, value: float):
        _, y, z = self._spherical_to_cartesian(self._r, self._theta, self._phi)
        self._r, self._theta, self._phi = self._cartesian_to_spherical(value, y, z)

    @property
    def y(self) -> float:
        _, y, _ = self._spherical_to_cartesian(self._r, self._theta, self._phi)
        return y

    @y.setter
    def y(self, value: float):
        x, _, z = self._spherical_to_cartesian(self._r, self._theta, self._phi)
        self._r, self._theta, self._phi = self._cartesian_to_spherical(x, value, z)

    @property
    def z(self) -> float:
        _, _, z = self._spherical_to_cartesian(self._r, self._theta, self._phi)
        return z

    @z.setter
    def z(self, value: float):
        x, y, _ = self._spherical_to_cartesian(self._r, self._theta, self._phi)
        self._r, self._theta, self._phi = self._cartesian_to_spherical(x, y, value)

    def distance_to(self, other: "Point") -> float:
        """
        Calculate distance to another point using spherical coordinates.
        Uses the spherical law of cosines for efficiency when both points
        are SphericalPoint instances.
        """
        if isinstance(other, SphericalPoint):
            if self._r == 0:
                return other._r
            if other._r == 0:
                return self._r

            # Spherical law of cosines for 3D
            cos_angle = (math.sin(self._theta) * math.sin(other._theta) *
                         math.cos(self._phi - other._phi) +
                         math.cos(self._theta) * math.cos(other._theta))

            # Clamp to [-1, 1] to handle floating point errors
            cos_angle = max(-1.0, min(1.0, cos_angle))

            return math.sqrt(self._r**2 + other._r**2 - 2 * self._r * other._r * cos_angle)
        else:
            # Fallback to Cartesian distance for other Point types
            dx = other.x - self.x
            dy = other.y - self.y
            dz = other.z - self.z
            return math.sqrt(dx**2 + dy**2 + dz**2)

    def direction_to(self, other: "Point") -> tuple[float, float]:
        """
        Calculate the angular direction (theta, phi) from this point toward another.
        Returns the angles in the local spherical coordinate system.
        """
        dx = other.x - self.x
        dy = other.y - self.y
        dz = other.z - self.z

        dist = math.sqrt(dx**2 + dy**2 + dz**2)
        if dist == 0:
            return 0.0, 0.0

        theta = math.acos(dz / dist)
        phi = math.atan2(dy, dx)
        return theta, phi

