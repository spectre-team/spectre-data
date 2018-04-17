""" ultilitels """

from .common import Name

def as_readable(dataset_name: str) -> Name:
    """Convert name on disk to readable for the user"""
    return dataset_name.replace('_', ' ')

class UnknownIdError(KeyError):
    """Thrown when id of element could not be resolved"""
    pass

class DatasetNotFoundError(IOError):
    """Thrown when dataset of given name could not be found"""
    def __init__(self, dataset_name):
        super().__init__('Dataset ' + dataset_name + ' could not be found.')

class UnsupportedExtensionError(IOError):
    """Thrown when file is of unsupported type"""
    def __init__(self, extension_name):
        super().__init__('Unsupported extension: ' + extension_name + ".")