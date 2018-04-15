import os

_FILESYSTEM_ROOT = os.path.abspath(os.sep)
DATA_ROOT = os.path.join(_FILESYSTEM_ROOT, 'data')
MAX_JAVASCRIPT_SAFE_INT = 2 ** 53 - 1

Name = str
Path = str