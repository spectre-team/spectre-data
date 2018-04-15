import os
import utility as util

from typing import List
from common import DATA_ROOT, Name, Path, Extension

def name(element_id: int, names: List[Name]) -> Name:
    """Resolve element name by its id
    :param element_id: id of the element in names list
    :param names: names list
    :return: name of the element under given id
    """
    matching = [_name for _name in names
                if util.name_to_id(_name) == element_id]
    if len(matching) == 0:
        raise util.UnknownIdError(element_id)
    return matching[0]

def list_datasets() -> List[Path]:
    return os.listdir(DATA_ROOT)

def data_path(dataset_name: Name) -> Path:
    """Discover path to dataset
    :param dataset_name: name of the dataset
    :return: path to the dataset file
    """
    return os.path.join(DATA_ROOT, dataset_name, 'text_data', 'data.txt')

################

from functools import partial
import json
import os
from typing import Callable, Dict, List, Optional

#from common import DATASETS_ROOT, Response, NOT_FOUND


def as_readable(dataset_name: str) -> Name:
    """Convert name on disk to readable for the user"""
    return dataset_name.replace('_', ' ')


def is_dir(root: Path, name: Name) -> bool:
    """Check if name is dataset name in root directory"""
    return os.path.isdir(os.path.join(root, name))


def get_datasets() -> List[Dict[Name, str]]:
    """"Get datasets available in the store"""
    is_dataset_name = partial(is_dir, DATA_ROOT)
    datasets = filter(is_dataset_name, list_datasets())
    return [{"name": as_readable(name), "value": name} for name in datasets]


def substitute_tags(tag_map: Dict[str, str], text: str) -> str:
    """Substitute tags from the text for corresponding values in the map"""
    for tag, value in tag_map.items():
        text = text.replace('"' + tag + '"', value)
    return text


Substitutor = Optional[Callable[[str], str]]


def datasets_substitutor() -> Substitutor:
    """Factory of datasets substitutor"""
    datasets = get_datasets()
    parsed = json.dumps(datasets)
    return partial(substitute_tags, {'$DATASETS': parsed})


SubstitutorFactory = Callable[[], Substitutor]


""" def file_from_disk(substitutor_factory: SubstitutorFactory, path: str) -> Response:
    \"\"\"Read file from disk with subsitutions and return it as HTTP response\"\"\"
    if not os.path.exists(path):
        return NOT_FOUND
    with open(path) as disk_file:
        content = disk_file.read()
    if substitutor_factory is None:
        return content, 200
    substitutor = substitutor_factory()
    substituted = substitutor(content)
    return substituted, 200 


file_with_datasets_substitution = partial(file_from_disk, datasets_substitutor)
unchanged_file = partial(file_from_disk, None) """

######################

def dataset_exists(name: Name) -> bool:
    all_datasets = get_datasets()
    return name in all_datasets.values()

