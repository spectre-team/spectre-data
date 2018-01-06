"""Reusable types across package"""


import numpy as np


class Coordinates:
    """X, Y, Z coordinates"""
    def __init__(self, x, y, z):
        """
        Args:
            x: x-coordinates for each spectrum
            y: y-coordinates for each spectrum
            z: z-coordinates for each spectrum

        Raises:
            ValueError
        """
        self.x = np.array(x)
        self.y = np.array(y)
        self.z = np.array(z)
        self._validate()

    def __len__(self):
        return self.x.size

    def _validate(self):
        if self.x.size != self.y.size:
            raise ValueError("Number of X and Y coordinates should be equal. "
                             "Was: %i and %i" % (self.x.size, self.y.size))
        if self.x.size != self.z.size:
            raise ValueError("Number of X and Z coordinates should be equal. "
                             "Was: %i and %i" % (self.x.size, self.z.size))
