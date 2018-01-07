import unittest

import spdata.types as ty


class TestCoordinates(unittest.TestCase):
    def test_throws_on_different_size_coordinates(self):
        with self.assertRaises(ValueError):
            ty.Coordinates(x=[1, 2], y=[3], z=[4, 5])
        with self.assertRaises(ValueError):
            ty.Coordinates(x=[1, 2], y=[3, 4], z=[5])
        with self.assertRaises(ValueError):
            ty.Coordinates(x=[1], y=[2, 3], z=[4, 5])


class TestDataset(unittest.TestCase):
    def setUp(self):
        self.coordinates = ty.Coordinates(x=[1, 2], y=[3, 4], z=[5, 6])
        self.short_coordinates = ty.Coordinates(x=[1], y=[2], z=[3])

    def test_throws_on_missing_coordinates(self):
        with self.assertRaises(ValueError):
            ty.Dataset(spectra=[[1, 2], [3, 4]],
                       coordinates=self.short_coordinates,
                       mz=[1.1, 2.2])

    def test_throws_on_missing_mzs(self):
        with self.assertRaises(ValueError):
            ty.Dataset(spectra=[[1, 2], [3, 4]], coordinates=self.coordinates,
                       mz=[1.1])

    def test_throws_on_mismatching_labels(self):
        with self.assertRaises(ValueError):
            ty.Dataset(spectra=[[1, 2], [3, 4]], coordinates=self.coordinates,
                       mz=[1.1, 2.2], labels=[9])
