from __future__ import annotations
from abc import ABC, abstractmethod


class Point(ABC):
    """
    Abstract base class for points in 3D space.
    Defines the interface for both Cartesian and spherical coordinate access.
    """

    # Cartesian coordinate properties (required for all point types)
    @property
    @abstractmethod
    def x(self) -> float:
        """X coordinate in Cartesian space."""
        pass

    @x.setter
    @abstractmethod
    def x(self, value: float):
        pass

    @property
    @abstractmethod
    def y(self) -> float:
        """Y coordinate in Cartesian space."""
        pass

    @y.setter
    @abstractmethod
    def y(self, value: float):
        pass

    @property
    @abstractmethod
    def z(self) -> float:
        """Z coordinate in Cartesian space."""
        pass

    @z.setter
    @abstractmethod
    def z(self, value: float):
        pass

    # Spherical coordinate properties (required for all point types)
    @property
    @abstractmethod
    def r(self) -> float:
        """Radial distance from origin."""
        pass

    @r.setter
    @abstractmethod
    def r(self, value: float):
        pass

    @property
    @abstractmethod
    def theta(self) -> float:
        """Polar angle from positive z-axis (0 to π)."""
        pass

    @theta.setter
    @abstractmethod
    def theta(self, value: float):
        pass

    @property
    @abstractmethod
    def phi(self) -> float:
        """Azimuthal angle in x-y plane (0 to 2π)."""
        pass

    @phi.setter
    @abstractmethod
    def phi(self, value: float):
        pass

    @abstractmethod
    def distance_to(self, other: "Point") -> float:
        """Calculate distance to another point."""
        pass

    @abstractmethod
    def direction_to(self, other: "Point") -> tuple[float, float]:
        """
        Calculate the angular direction (theta, phi) from this point toward another.
        Returns the angles representing the direction vector.
        """
        pass

