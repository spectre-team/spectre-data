"""Various methods for reading data"""

from typing import List, Tuple
import numpy as np

import spdata.types as ty
from pyimzml.ImzMLParser import ImzMLParser as imzparse

def _parse_metadata(line: str) -> (int, int, int, int):
    x, y, z, label, *_ = line.split()
    return int(x), int(y), int(z), int(label)


def _parse_data(line: str) -> List[float]:
    return [float(value) for value in line.split()]


def _load_entry(metadata_line: str, data_line: str) -> Tuple[
        Tuple[int, int, int], int, List[float]]:
    x, y, z, label = _parse_metadata(metadata_line)
    data = _parse_data(data_line)
    return (x, y, z), label, data


def load_txt(content) -> ty.Dataset:
    """Load Dataset from file

    Args:
        content (iterable): data file content

    Returns:
        out: spdata.types.Dataset
    """
    iterator = iter(content)
    _ = next(iterator)  # unsupported global metadata
    mzs_line = next(iterator)

    mzs = [float(mz) for mz in mzs_line.split()]

    entries = map(_load_entry, iterator, iterator)

    coordinates, labels, data = zip(*entries)

    data = np.vstack(data)
    coordinates = ty.Coordinates(*zip(*coordinates))

    return ty.Dataset(data, coordinates, mzs, labels)

def load_imzml(file_path) -> ty.Dataset:
    """Load Dataset from imzml file

    Args:
        file_path: path to imzml file

    Returns:
        out: spdata.types.Dataset
    """
    with imzparse(file_path) as input_handle:
        assert np.min(input_handle.mzLengths) == np.max(input_handle.mzLengths)
        mzs = input_handle.getspectrum(0)[0]
        spectra = [
            input_handle.getspectrum(i)[1]
            for i in range(len(input_handle.coordinates))
        ]
        coordinates = [
            (x, y, z)
            for idx, (x, y, z) in enumerate(input_handle.coordinates)
        ]
        coordinates = list(map(list, zip(*coordinates)))
        return ty.Dataset(spectra, ty.Coordinates(coordinates[0], coordinates[1], coordinates[2]), mzs)
