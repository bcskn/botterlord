import os
"""Get self file path."""

def get_path(filename):
    _path = os.path.realpath('main.py')
    _lenpath = len(_path)
    _lenpath -= 7
    _path = _path[:_lenpath]
    _path = _path + filename
    return _path
