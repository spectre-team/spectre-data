import hashlib
from functools import lru_cache
from common import MAX_JAVASCRIPT_SAFE_INT

@lru_cache(maxsize=1024)
def name_to_id(entity_name: str) -> int:
    """Get ID for a name
    Computes SHA256 hash of name and converts it to int value.
    :param entity_name: name of an object
    :return: unique identifier
    """
    hex_hash = hashlib.sha256(entity_name.encode()).hexdigest()
    return int(hex_hash, 16) % MAX_JAVASCRIPT_SAFE_INT

class UnknownIdError(KeyError):
    """Thrown when id of element could not be resolved"""
    pass

class DatasetNotFound(IOError):
    """Thrown when dataset of given name could not be found"""
    def __init__(self, dataset_name):
        super().__init__('Dataset ' + dataset_name + ' could not be found.')

class UnsupportedExtension(IOError):
    """Thrown when file is of unsupported type"""
    def __init__(self, extension_name):
        super().__init__('Unsupported extension: ' + extension_name + ".")