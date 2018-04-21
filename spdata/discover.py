"""Methods providing functionality for dataset discovery across the filesystem"""

import os

from typing import Callable, Dict, List, Optional, Union
from functools import partial, lru_cache
from hashlib import sha256
from glob import glob

from .utility import as_readable, UnknownIdError
from .common import DATA_ROOT, Name, Path

MAX_JAVASCRIPT_SAFE_INT = 2 ** 53 - 1

@lru_cache(maxsize=1024)
def name_to_id(entity_name: str) -> int:
    """Get ID for a name
    Computes SHA256 hash of name and converts it to int value.

    Args:
        entity_name: name of an object

    Returns:
        out: unique identifier
    """
    hex_hash = sha256(entity_name.encode()).hexdigest()
    return int(hex_hash, 16) % MAX_JAVASCRIPT_SAFE_INT

def id_to_name(element_id: int) -> Name:
    """Resolve element name by its id
    Args:
        element_id: id of the element in names list

    Returns:
        out: name of the element under given id
    """
    matching = [_name for _, _name in enumerate(d['name'] for d in get_datasets())
                if name_to_id(_name) == element_id]
    if len(matching) == 0:
        raise UnknownIdError(element_id)
    return matching[0]

def dataset_path(dataset_name: Name) -> Union[Path, List[Path]]:
    """Discover path to dataset
    Args:
        dataset_name: name of the dataset

    Returns:
        out: path to the dataset file
    """
    name_root = os.path.join(DATA_ROOT, dataset_name)
    file_list = glob(os.path.join(name_root, '*_data', '*.*'))
    if len(file_list) == 1:
        return file_list[1]
    else:
        return file_list

def get_datasets() -> List[Dict[Name, str]]:
    """"Get datasets available in the store
    Returns:
        out: list of dataset entries
    """
    def is_dir(root: Path, name: Name) -> bool:
        return os.path.isdir(os.path.join(root, name))
    is_dataset_name = partial(is_dir, DATA_ROOT)
    datasets = filter(is_dataset_name, os.listdir(DATA_ROOT))
    return [{"name": as_readable(name), "value": name} for name in datasets]

def dataset_exists(name: Name) -> bool:
    """Discover path to dataset
    Args:
        name: name of the dataset
        
    Returns:
        out: True if dataset is in the filesystem, False otherwise
    """
    all_datasets = get_datasets()
    name_list = [_name for _, _name in enumerate(d['name'] for d in all_datasets)]
    return name in name_list