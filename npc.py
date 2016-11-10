"""Code where npc and info about <rumors> will be handled."""
import sqlite3
import world

def add_npc_db(_addr, _npc):
    """Update node column npc."""
    conn = sqlite3.connect('botterlord.db')
    db = conn.cursor()
    _valdb = (_npc, _addr)
    db.execute("""\
        UPDATE NODES
        SET NPC = ?
        WHERE ADDR = ?
        """, _valdb)
    conn.commit()
    conn.close()

class npc:
    def __init__(self, _name, _loc):
        self.name = _name
        self.loc = _loc #address of the node it resides in
        self.actions = {}
        add_colnpc(_loc, _name)
    def add_action(self, _act_name, _act):
        self.actions[_act_name] = _act

def call_npc(name, acto):
    name = name.lower()
    if name == 'george':
        if acto == 'idle':
            return George.idle
        if acto == 'greet':
            return George.greet

'''//////////////////SPECIAL NPCS/////////////////////'''

class George:
    idle = "This is the test idle text for George."
    greet = "This is the talk/greet message."


#Debug Area
add_npc_db('10:40', 'George')
print world.chcknode('10:40', 'NPC')
print call_npc('george', 'greet')
