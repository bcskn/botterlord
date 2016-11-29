import os

def get_path(filename = 'main.pt'):
    """Get self file path."""
    _path = os.path.realpath('main.py')
    _lenpath = len(_path)
    _lenpath -= 7
    _path = _path[:_lenpath]
    _path = _path + filename
    return _path

def parse_str_loc(strloc):
    strloc = strloc.split(':')
    return strloc[0], strloc[1]
