"""File for setting up adventures and information in nodes."""
import sqlite3
import yaml
import tools


def add_ncolumn(tab_name, col_name, col_type, df_val): # Items, exits columns are also needed.
    """Add a new column with default value."""
    conn = sqlite3.connect('botterlord.db')
    db = conn.cursor()
    try:
        db.execute(" ALTER TABLE {tn} \
            ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
            .format(tn=tab_name, cn=col_name, ct=col_type, df=df_val))
    except:
        print 'world: Column already exists.'
        pass
    conn.commit()
    conn.close()

def chcknode(_addr, _rtrn):
    """Check adventure and npc columns."""
    str_node = get_node(_addr)

    if _rtrn == 'NPC':
        rtrn = str_node[2]
    if _rtrn == 'ADVE':
        rtrn = str_node[3]
    return rtrn

def get_node(_addr_):
    """Fetch a node from the database file."""
    conn = sqlite3.connect('botterlord.db')
    db = conn.cursor()
    _addrdb_ = (_addr_,)
    db.execute('SELECT * FROM NODES WHERE ADDR = ?', _addrdb_)
    return db.fetchone()
    conn.commit()
    conn.close()

def chck_bot_exist(np_row, np_col, world_file): # No errors
    """Check if there is a bot in given coordinates stored inside the world file."""
    with open(world_file, 'r') as stream:
        profile = yaml.load(stream)
        for bot_key in profile:
            if 'loc' in profile[bot_key]:
                print 'loc in bot_key = True', profile[bot_key]
                addr = tools.parse_str_loc(profile[bot_key]['loc'])
                chkd_row = int(addr[0]); chkd_col = int(addr[1])
                if np_row == chkd_row and np_col == chkd_col:
                    return True
                else:
                    return False


def show_bots(filesname): #WHY
    """Returns a list with all the bot locations in it."""
    stream__ = open(filesname, 'r')
    prof__ = yaml.load(stream__)
    bot_adrs = [] # It's a list
    for keyval in prof__: # Go through dictionaries in yaml file.
        if keyval.startswith('bot_') == False: # If it doesn't start with bot_
            continue # Go back and check another one.
        else:
            bot_adrs.append(prof__[keyval]['loc'])
    return bot_adrs
print show_bots('worlds\profile.yml')
