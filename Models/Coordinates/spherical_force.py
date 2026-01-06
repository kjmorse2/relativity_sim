from __future__ import annotations
import math


class SphericalForce:
    """
    Force stored in spherical coordinates (F_r, F_theta, F_phi).
    - F_r: radial force component
    - F_theta: polar angular force component
    - F_phi: azimuthal angular force component

    This representation is ideal for gravitational calculations where
    force is primarily radial.
    """

    def __init__(self, F_r: float = 0.0, F_theta: float = 0.0, F_phi: float = 0.0):
        self._F_r = F_r
        self._F_theta = F_theta
        self._F_phi = F_phi

    @property
    def F_r(self) -> float:
        """Radial force component."""
        return self._F_r

    @F_r.setter
    def F_r(self, value: float):
        self._F_r = value

    @property
    def F_theta(self) -> float:
        """Polar angular force component."""
        return self._F_theta

    @F_theta.setter
    def F_theta(self, value: float):
        self._F_theta = value

    @property
    def F_phi(self) -> float:
        """Azimuthal angular force component."""
        return self._F_phi

    @F_phi.setter
    def F_phi(self, value: float):
        self._F_phi = value

    def __add__(self, other: "SphericalForce") -> "SphericalForce":
        """Add two spherical forces."""
        return SphericalForce(
            self._F_r + other._F_r,
            self._F_theta + other._F_theta,
            self._F_phi + other._F_phi
        )

    def __mul__(self, scalar: float) -> "SphericalForce":
        """Multiply force by a scalar."""
        return SphericalForce(
            self._F_r * scalar,
            self._F_theta * scalar,
            self._F_phi * scalar
        )

    def __rmul__(self, scalar: float) -> "SphericalForce":
        return self.__mul__(scalar)

    def magnitude(self) -> float:
        """Calculate the magnitude of the force."""
        return math.sqrt(self._F_r**2 + self._F_theta**2 + self._F_phi**2)

    def reset(self):
        """Reset all force components to zero."""
        self._F_r = 0.0
        self._F_theta = 0.0
        self._F_phi = 0.0

    def __repr__(self) -> str:
        return f"SphericalForce(F_r={self._F_r}, F_theta={self._F_theta}, F_phi={self._F_phi})"

