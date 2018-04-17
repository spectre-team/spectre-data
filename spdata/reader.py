"""Various methods for reading data"""

import os

from typing import List, Tuple, Union
from common import Name, Path

import numpy as np
import discover as disc
import pyimzml.ImzMLParser as imzparse

from . import types as ty

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

# Definition of loaders
from functools import wraps
loaders = {}

def Loader(ext: str):
    def register_loader(f):
        loaders.setdefault(ext, f)
        @wraps(f)
        def loader_wrapper(file_path: Path):
            return f(file_path)
        return loader_wrapper
    return register_loader

@Loader('.txt')
def load_txt(file_path: Path) -> ty.Dataset:
    """Load Dataset from file

    Args:
        file_path : data file path

    Returns:
        out: spdata.types.Dataset
    """
    content = os.open(file_path).load_txt()

    iterator = iter(content)
    _ = next(iterator)  # unsupported global metadata
    mzs_line = next(iterator)

    mzs = [float(mz) for mz in mzs_line.split()]

    entries = map(_load_entry, iterator, iterator)

    coordinates, labels, data = zip(*entries)

    data = np.vstack(data)
    coordinates = ty.Coordinates(*zip(*coordinates))

    return ty.Dataset(data, coordinates, mzs, labels)

@Loader('.imzml')
def imzml(file_path: Path) -> ty.Dataset:
    """Load Dataset from imzml file

    Args:
        file_path: path to imzml file

    Returns:
        out: spdata.types.Dataset
    """
    with imzparse.ImzMLParser(file_path) as input_handle:
        if np.min(input_handle.mzLengths) != np.max(input_handle.mzLengths):
            raise ValueError("Can't read processed data.")
        mzs = input_handle.getspectrum(0)[0]
        coordinates = [
            (x, y, z)
            for idx, (x, y, z) in enumerate(input_handle.coordinates)
        ]
        spectra = [
            input_handle.getspectrum(i)[1]
            for i in range(len(coordinates))
        ]
        coordinates = ty.Coordinates(*zip(*coordinates))
        return ty.Dataset(spectra, coordinates, mzs)


def load_dataset(name: Name, allow_multiple=False) -> Union[ty.Dataset, List[ty.Dataset]]:
    def fetch_dataset(dataset_path : Path):
        _, extension = os.path.splitext(dataset_path)
        if extension not in loaders.keys():
            raise IOError('Unsupported type: ' + extension + ".")
        return loaders[extension](dataset_path)
    if not disc.dataset_exists(name):
        raise IOError('Dataset ' + name + ' could not be found.')
    path = disc.dataset_path(name)
    if type(path) is List and allow_multiple == True:
        result_multiple = []
        for entry in path:
            result_multiple.append(fetch_dataset(entry))
        return result_multiple
    return fetch_dataset(path)
    