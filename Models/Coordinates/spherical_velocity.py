from __future__ import annotations
import math

from .point import Point


class SphericalVelocity:
    """
    Velocity stored in spherical coordinates (v_r, v_theta, v_phi).
    - v_r: radial velocity (rate of change of r)
    - v_theta: polar angular velocity (rate of change of theta)
    - v_phi: azimuthal angular velocity (rate of change of phi)

    This representation is ideal for gravitational simulations where
    radial motion is often the dominant component.
    """

    def __init__(self, v_r: float, v_theta: float, v_phi: float):
        self._v_r = v_r
        self._v_theta = v_theta
        self._v_phi = v_phi

    @classmethod
    def from_cartesian(cls, vx: float, vy: float, vz: float,
                       position: Point) -> "SphericalVelocity":
        """
        Convert Cartesian velocity to spherical velocity at a given position.
        :param vx: x-component of velocity
        :param vy: y-component of velocity
        :param vz: z-component of velocity
        :param position: the position at which the velocity is defined
        """
        r = position.r
        theta = position.theta
        phi = position.phi

        if r == 0:
            # At origin, velocity is purely radial in the direction of motion
            speed = math.sqrt(vx**2 + vy**2 + vz**2)
            return cls(speed, 0.0, 0.0)

        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)
        sin_phi = math.sin(phi)
        cos_phi = math.cos(phi)

        # Transform Cartesian velocity to spherical velocity components
        v_r = (vx * sin_theta * cos_phi +
               vy * sin_theta * sin_phi +
               vz * cos_theta)

        v_theta = (vx * cos_theta * cos_phi +
                   vy * cos_theta * sin_phi -
                   vz * sin_theta) / r if r > 0 else 0.0

        v_phi = (-vx * sin_phi + vy * cos_phi) / (r * sin_theta) if (r > 0 and sin_theta != 0) else 0.0

        return cls(v_r, v_theta, v_phi)

    def to_cartesian(self, position: Point) -> tuple[float, float, float]:
        """
        Convert spherical velocity to Cartesian velocity at a given position.
        :param position: the position at which the velocity is defined
        :return: tuple of (vx, vy, vz)
        """
        r = position.r
        theta = position.theta
        phi = position.phi

        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)
        sin_phi = math.sin(phi)
        cos_phi = math.cos(phi)

        # Transform spherical velocity to Cartesian velocity components
        vx = (self._v_r * sin_theta * cos_phi +
              r * self._v_theta * cos_theta * cos_phi -
              r * sin_theta * self._v_phi * sin_phi)

        vy = (self._v_r * sin_theta * sin_phi +
              r * self._v_theta * cos_theta * sin_phi +
              r * sin_theta * self._v_phi * cos_phi)

        vz = (self._v_r * cos_theta -
              r * self._v_theta * sin_theta)

        return vx, vy, vz

    @property
    def v_r(self) -> float:
        """Radial velocity component."""
        return self._v_r

    @v_r.setter
    def v_r(self, value: float):
        self._v_r = value

    @property
    def v_theta(self) -> float:
        """Polar angular velocity component."""
        return self._v_theta

    @v_theta.setter
    def v_theta(self, value: float):
        self._v_theta = value

    @property
    def v_phi(self) -> float:
        """Azimuthal angular velocity component."""
        return self._v_phi

    @v_phi.setter
    def v_phi(self, value: float):
        self._v_phi = value

    def magnitude(self, position: Point) -> float:
        """
        Calculate the speed (magnitude of velocity) at the given position.
        :param position: the position at which to calculate the speed
        :return: the scalar speed
        """
        r = position.r
        sin_theta = math.sin(position.theta)

        # |v|² = v_r² + (r * v_theta)² + (r * sin(theta) * v_phi)²
        return math.sqrt(
            self._v_r**2 +
            (r * self._v_theta)**2 +
            (r * sin_theta * self._v_phi)**2
        )

    def __add__(self, other: "SphericalVelocity") -> "SphericalVelocity":
        """Add two spherical velocities."""
        return SphericalVelocity(
            self._v_r + other._v_r,
            self._v_theta + other._v_theta,
            self._v_phi + other._v_phi
        )

    def __mul__(self, scalar: float) -> "SphericalVelocity":
        """Multiply velocity by a scalar."""
        return SphericalVelocity(
            self._v_r * scalar,
            self._v_theta * scalar,
            self._v_phi * scalar
        )

    def __rmul__(self, scalar: float) -> "SphericalVelocity":
        """Right multiply velocity by a scalar."""
        return self.__mul__(scalar)

    def __repr__(self) -> str:
        return f"SphericalVelocity(v_r={self._v_r}, v_theta={self._v_theta}, v_phi={self._v_phi})"
