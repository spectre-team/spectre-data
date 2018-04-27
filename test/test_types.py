"""Test for types module

Copyright 2018 Spectre Team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
    
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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
