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

def fit_title(size):
    title = ""
    if size < 1920:
        title = """\
         ____        _   _            _                  _
        | __ )  ___ | |_| |_ ___ _ __| |    ___  _ __ __| |
        |  _ \ / _ \| __| __/ _ \ '__| |   / _ \| '__/ _` |
        | |_) | (_) | |_| ||  __/ |  | |__| (_) | | | (_| |
        |____/ \___/ \__|\__\___|_|  |_____\___/|_|  \__,_|
        """
    if size < 1600:
        title = """\
        _
        |_) _ _|__|_ _  __|   _  __ _|
        |_)(_) |_ |_(/_ | |__(_) | (_|
        """
    return title
