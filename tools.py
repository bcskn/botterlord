import os
"""Get self file path."""

def get_path(filename = None):
    _path = os.path.realpath('main.py')
    _lenpath = len(_path)
    _lenpath -= 7
    _path = _path[:_lenpath]
    if filename != None:
        _path = _path + filename
    return _path

def parse_str_loc(strloc):
    strloc = strloc.split(':')
    return strloc[0], strloc[1]
