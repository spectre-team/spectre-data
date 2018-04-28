"""Various methods for reading data

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

import os

from typing import List, Tuple, Callable
from functools import wraps

import numpy as np
import pyimzml.ImzMLParser as imzparse

from . import types as ty
from . import discover as disc
from .common import Name, Path

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
loaders = {}

def loader(ext: str):
    def register_loader(f : Callable[[Path], ty.Dataset]):
        loaders.setdefault(ext, f)
        @wraps(f)
        def loader_wrapper(file_path: Path):
            return f(file_path)
        return loader_wrapper
    return register_loader

@loader('.txt')
def load_txt(file_path: Path) -> ty.Dataset:
    """Load Dataset from file.

    Args:
        file_path : Data file path.

    Returns:
        spdata.types.Dataset
    """
    with open(file_path) as f:
        iterator = iter(f)
        _ = next(iterator)  # unsupported global metadata
        mzs_line = next(iterator)

        mzs = [float(mz) for mz in mzs_line.split()]

        entries = map(_load_entry, iterator, iterator)

        coordinates, labels, data = zip(*entries)

        data = np.vstack(data)
        coordinates = ty.Coordinates(*zip(*coordinates))

    return ty.Dataset(data, coordinates, mzs, labels)

@loader('.imzml')
def load_imzml(file_path: Path) -> ty.Dataset:
    """Load Dataset from imzml file.

    Args:
        file_path: Path to imzml file.

    Returns:
        The dataset itself.
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


def load_dataset(name: Name) -> ty.Dataset:
    """Generic, universal method for loading single dataset of arbitrary registered format.

    Args:
        name: Name of desired dataset.

    Returns:
        The dataset itself.
    
    """
    if not disc.dataset_exists(name):
        raise IOError('Dataset ' + name + ' could not be found.')
    path = disc.dataset_path(name)
    _, extension = os.path.splitext(path)
    if extension not in loaders.keys():
        raise IOError('Unsupported type: ' + extension + ".")
    return loaders[extension](path)
    