""" ultilitels """

from .common import Name

def as_readable(dataset_name: str) -> Name:
    """Convert name on disk to readable for the user"""
    return dataset_name.replace('_', ' ')

class UnknownIdError(KeyError):
    """Thrown when id of element could not be resolved"""
    pass