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


class Dataset:
    """Simplistic common interface for MSI data"""
    # @gmrukwa: types purposefully left blank to preserve flexibility
    def __init__(self, spectra, coordinates: Coordinates, mz, labels=None):
        """
        Args:
            spectra: measured values of spectra with spectra in rows and mass
            channels in columns
            coordinates (Coordinates): coordinates for each spectrum
            mz: values of m/z for mass channels
            labels: optional labels for spectra

        Raises:
            ValueError
        """
        self.spectra = np.array(spectra)
        self.coordinates = coordinates
        self.mz = np.array(mz)
        self.labels = np.array(labels) if labels is not None else None
        self._validate()

    def _validate(self):
        if self.labels is not None and self.labels.size != len(
                self.coordinates):
            raise ValueError("Number of labels and coordinates should be equal."
                             " Was: %i and %i"
                             % (self.labels.size, len(self.coordinates)))
        if self.spectra.shape[0] != len(self.coordinates):
            raise ValueError("Number of spectra should be equal number of "
                             "coordinates. Were: %i and %i"
                             % (self.spectra.shape[0], len(self.coordinates)))
        if self.spectra.shape[1] != self.mz.size:
            raise ValueError("Number of features spectra should be equal "
                             "number of m/z-s registered. Were: %i and %i"
                             % (self.spectra.shape[1], self.mz.size))
