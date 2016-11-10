import os
import sqlite3


def remv_file(filename):
    _path = os.path.realpath('main.py')
    _lenpath = len(_path)
    _lenpath -= 7
    _path = _path[:_lenpath]
    _path = _path + filename
    os.remove(_path)

remv_file('botterlord.db')   #  RENEW DATABASE

conn = sqlite3.connect('botterlord.db')
db = conn.cursor()

try:
    db.execute(''' \
        CREATE TABLE NODES
        (
        ADDR TEXT,
        REPR TEXT,
        NPC TEXT
        )
    ;''')
except:
    print "Node table <NODES> already exists."

try:
    """The basic settings of an npc. There might be more intereaction options
    and it's possible to add them with the add_ncolumn function."""
    db.execute(''' \
        CREATE TABLE NPCS
        (
        ID INTEGER PRIMARY KEY NOT NULL,
        NAME TEXT NOT NULL,
        ACTO TEXT
        )
    ;''')
except:
    print "Node table <NPCS> already exists."
import botmap
import world

botmap.map_scan()
world.add_ncolumn('NODES', 'ADVE', 'TEXT', 'None')
