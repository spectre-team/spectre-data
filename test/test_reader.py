"""Test for reader module

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
import io
import os
import pyimzml.ImzMLParser as imzparse
import numpy.testing as npt
import numpy as np
import spdata.reader as rd
from unittest.mock import patch
from unittest.mock import MagicMock

class TestParseMetadata(unittest.TestCase):
    def test_extracts_coordinates_as_ints(self):
        x, y, z, _ = rd._parse_metadata('1 2 3 4')
        self.assertEqual(x, 1)
        self.assertEqual(y, 2)
        self.assertEqual(z, 3)
        self.assertIsInstance(x, int)
        self.assertIsInstance(y, int)
        self.assertIsInstance(z, int)

    def test_extracts_label_as_int(self):
        *_, label = rd._parse_metadata('1 2 3 4')
        self.assertEqual(label, 4)
        self.assertIsInstance(label, int)

    def test_throws_out_redundant_data(self):
        self.assertEqual(len(rd._parse_metadata('1 2 3 4 5')), 4)


class TestParseData(unittest.TestCase):
    def test_extracts_intensities_as_floats(self):
        intensities = rd._parse_data('1.2 3.4 5.6')
        self.assertSequenceEqual([1.2, 3.4, 5.6], intensities)
        for value in intensities:
            self.assertIsInstance(value, float)


class TestLoadTxt(unittest.TestCase):
    def setUp(self):
        self.expected_mz = [1.2, 3.4, 5.6]
        self.expected_spectra_number = 2
        self.expected_spectra = [
            [12.3, 45.6, 78.9],
            [98.7, 65.4, 32.1]
        ]
        self.expected_xs = [12, 56]
        self.expected_ys = [34, 78]
        self.expected_zs = [56, 90]
        self.test_file = io.StringIO("""global metadata to throw out
1.2 3.4 5.6
12 34 56 78 11 a f 4 6 h
12.3 45.6 78.9
56 78 90 12 1 4 7 h 3 h more garbage
98.7 65.4 32.1
""")

    @patch('os.open')
    def test_loads_mzs(self, mock_open):
        mock_open.return_value = self.test_file
        data = rd.load_txt('some_path.txt')
        npt.assert_equal(data.mz, self.expected_mz)

    @patch('os.open')
    def test_loads_all_spectra(self, mock_open):
        mock_open.return_value = self.test_file
        data = rd.load_txt('some_path.txt')
        self.assertEqual(data.spectra.shape[0], self.expected_spectra_number)
        for spectrum, expected in zip(data.spectra, self.expected_spectra):
            npt.assert_equal(spectrum, expected)

    @patch('os.open')
    def test_loads_all_coordinates(self, mock_open):
        mock_open.return_value = self.test_file
        data = rd.load_txt('some_path.txt')
        npt.assert_equal(data.coordinates.x, self.expected_xs)
        npt.assert_equal(data.coordinates.y, self.expected_ys)
        npt.assert_equal(data.coordinates.z, self.expected_zs)

class MockParser:
    def __init__(self, _):
        self.mzs = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        self.intensities = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.coordinates = [(1, 1, 1), (2, 2, 2), (3, 3, 3)]
        self.mzLengths = map(len, self.mzs)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass
    
    def getspectrum(self, idx):
        return (self.mzs[idx], self.intensities[idx])
    
class TestLoadImzML(unittest.TestCase):
    def setUp(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = "tests.imzML"
        self.file_path = os.path.join(this_dir, file_name)
    
    # Test file will be provided during integration tests.
    # Link to the file: https://drive.google.com/drive/folders/1o02-7MJxW1ZsnC2iuHNlOy6zHpg8-q_2")
    def test_loads_file(self):
        mock = MockParser('')
        with patch.object(imzparse, 'ImzMLParser', new=MockParser):
            dataset = rd.load_imzml(self.file_path)

            npt.assert_equal(dataset.mz, np.array(mock.mzs[0])) 
            npt.assert_equal(dataset.spectra, np.array(mock.intensities))

            returnedCoords = list(zip(*mock.coordinates))
            npt.assert_equal(dataset.coordinates.x, np.array(returnedCoords[0]))
            npt.assert_equal(dataset.coordinates.y, np.array(returnedCoords[1]))
            npt.assert_equal(dataset.coordinates.z, np.array(returnedCoords[2]))

class TestGenericLoad(unittest.TestCase):
    def setUp(self):
        self.test_datasets = [
            { "name": "dataset number one", "value": "dataset_number_one"},
            { "name": "dataset number two", "value": "dataset_number_two"},
            { "name": "dataset number three", "value": "dataset_number_three"}
        ]

    @patch("spdata.discover.get_datasets")
    def test_throws_on_nonexistent_dataset(self, mock_get):
        mock_get.return_value = self.test_datasets
        with self.assertRaises(IOError):
            rd.load_dataset("dataset number four")
