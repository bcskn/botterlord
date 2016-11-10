"""File for setting up adventures and information in nodes."""
import sqlite3

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
    print str_node

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
