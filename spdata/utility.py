"""Miscellaneous helpers and exceptions for the package

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

from .common import Name

def as_readable(dataset_name: str) -> Name:
    """Convert name on disk to readable for the user"""
    return dataset_name.replace('_', ' ')

class UnknownIdError(KeyError):
    """Thrown when id of element could not be resolved"""
    pass