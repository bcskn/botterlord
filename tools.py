import os, platform
from screeninfo import get_monitors
"""Get self file path."""

def get_monitor_size():
    """Incidentally gets only the first given monitor, which we will assume
    where the software is running at."""
    for monitors in get_monitors():
        screen_size = monitors
        break
    screen_size = str(screen_size)
    crop_start = screen_size.find("(") + 1
    crop_end = screen_size.find("+")
    screen_size = screen_size[crop_start:crop_end]
    screen_size = screen_size.split("x")
    screen_size = {"width": int(screen_size[0]), "height": int(screen_size[1])}
    return screen_size

def get_path(filename = None):
    print type(platform.system())
    if platform.system() == "Windows":
        separator = "\\"
    else:
        separator = "/"
    try:
        filename = filename.split('/') #For in code expressions
    except:
        pass
    _path = os.path.realpath('main.py')
    _lenpath = len(_path)
    _lenpath -= 8
    _path = _path[:_lenpath]
    if filename != None:
        for i in filename:
            if i != None:
                _path = _path + separator + i
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
