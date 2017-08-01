import pytest
from pathlib import Path
from botterlord import cmd, tools, ymlr

input_log = ['start', 'newprofile', 'quit', 'yes']

def test_last_input():
    assert cmd.previous_command(input_log) == 'quit'
def legal_command_find():
    assert cmd.find_command("sta") == 'start'
def test_get_path():
    path_ = tools.get_path("texts/texts.yml")
    q = Path(path_)
    print q
    assert q.exists() == True
