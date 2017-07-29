# -*- coding: utf-8 -*-
import os, platform
from screeninfo import get_monitors
from pathlib import *
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
    if platform.system() == "Windows":
        separator = "\\"
    else:
        separator = "/"
    try:
        filename = filename.split('/') #For in code expressions
    except:
        pass
    _path = Path.cwd()

    if filename != None:
        for i in filename:
            if i != None:
                _path = PurePath(_path, i)
    _path = str(_path)
    return _path

print get_path("texts/texts.yml")

def parse_str_loc(strloc):
    strloc = strloc.split(':')
    return strloc[0], strloc[1]
