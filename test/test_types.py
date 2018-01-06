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
