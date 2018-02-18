import unittest
import io
import os
import pyimzml.ImzMLParser as imzparse
import numpy.testing as npt
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

    def test_loads_mzs(self):
        data = rd.load_txt(self.test_file)
        npt.assert_equal(data.mz, self.expected_mz)

    def test_loads_all_spectra(self):
        data = rd.load_txt(self.test_file)
        self.assertEqual(data.spectra.shape[0], self.expected_spectra_number)
        for spectrum, expected in zip(data.spectra, self.expected_spectra):
            npt.assert_equal(spectrum, expected)

    def test_loads_all_coordinates(self):
        data = rd.load_txt(self.test_file)
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
        with patch.object(imzparse, 'ImzMLParser', new=MockParser):
            rd.load_imzml(self.file_path)
