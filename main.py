#!python
# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
import yaml
from Tkinter import *
#-----------------------
import cmd
import botmap
import world
import npc
import ymlr
import tools
import path
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
'''------------Values--------------'''
'''/Hardcoded/'''
topbar_name = 'BotterLord DEV Version'
icon_name = 'Botter_logo.ico'  # Icon must be in .ico format.
map_frame_height = 475
bot_frame_height = 475
bot_frame_width = 900
window_minimum_height = 300
window_minimum_width = 1000
window_background_color = 'gray50'
map_font_size = 13
bot_font_size = 15
map_width = 64
map_height = 20
#----------------------------------------------
default_hp = 100
default_mp = 100
default_loc = '10:44'

'''------Get Icon Location------'''
_icon_path = path.get_path() + 'images\\' + icon_name # Retrieve image from images folder.

'''-----Connect to the Database-----'''
conn = sqlite3.connect('botterlord.db')
db = conn.cursor()

'''-----Variables-----'''
start = 1.0 #Start Line
fs_var = 0 #Fullscreen state
real_input = ''
real_parsed = ''

'''----- Variables stored in profile (yaml) file-----'''
world_file = ''
profile_name = '' # Loaded profile file and world name
bots = {}
bot_avatar = '<OO>' # Controlled bot sign
np_bot_avatar = '<oo>' # Uncontrolled bot sign
pc_name = '' # Name of the bot being controlled.
pc_row = 10
pc_col = 40

#---------------------------------------------
started = False #In title screen
waiting_value = False
name_entered = False
last_input = '' # The last entered command

botter_title = """\
╔══════════════════════════════════════════════════════════════════════════════════════╗
║ ██████╗  ██████╗ ████████╗████████╗███████╗██████╗ ██╗      ██████╗ ██████╗ ██████╗  ║
║ ██╔══██╗██╔═══██╗╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗ ║
║ ██████╔╝██║   ██║   ██║      ██║   █████╗  ██████╔╝██║     ██║   ██║██████╔╝██║  ██║ ║
║ ██╔══██╗██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗██║     ██║   ██║██╔══██╗██║  ██║ ║
║ ██████╔╝╚██████╔╝   ██║      ██║   ███████╗██║  ██║███████╗╚██████╔╝██║  ██║██████╔╝ ║
║ ╚═════╝  ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝  ║
╚══════════════════════════════════════════════════════════════════════════════════════╝ v_DEV
"""
entry_message = """\
\n Welcome to the BotterLord (dev version) \
\n                  \
\n Insert a command \
\n --------------- \
\n Start\
\n Load\
\n Quit\
\n --------------- \
"""
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
'''----------------Window Setup----------------'''

root = Tk() #Main Frame
root.title(topbar_name)
root.iconbitmap(_icon_path) #Window icon
root.minsize(window_minimum_width, window_minimum_height)
root.configure(background=window_background_color)
if root.state('zoomed') == False:
    root.state('zoomed')

#Relief is for widget "style"
map_frame = Frame(root,bg = "Black",relief=FLAT, height=map_frame_height)
bot_frame = Frame(root,bg = "Black",relief=FLAT, height=bot_frame_height, width=bot_frame_width)
text_field = Text(root,bg = "Black", fg="White",relief=FLAT)
bot_field = Text(bot_frame,bg = "Black", fg="White",relief=FLAT)
map_field = Text(map_frame,bg = "Black", fg="White",relief=FLAT)
textentry = Entry(root, bg = "Black", fg = "White", relief=FLAT)
scrollbar = Scrollbar(root, bg = "Black", relief=FLAT)
map_frame.grid(row=1, column=1, sticky=W+E+N+S)
bot_frame.grid(row=0, column=1, sticky=W+E+N+S, pady=(8,8))
map_frame.grid_propagate(False)
bot_frame.grid_propagate(False)

text_field.grid(row=0,column=0,rowspan=2,sticky=W+E+N+S, padx = (8, 8), pady = (8, 0))
bot_field.grid(sticky=W+E+N+S)
map_field.grid(sticky=W+E+N+S)
textentry.grid(row=2,column=0,columnspan=3,sticky=E+W, padx = 8, pady = 8)
scrollbar.grid(row=0,column=2,rowspan=2, sticky=E+N+S, padx=(8,8), pady=(8,0))

text_field.config(insertbackground="White",yscrollcommand=scrollbar.set, borderwidth = 10 )
bot_field.config(insertbackground="White", borderwidth = 10, font=('Lucida Console', bot_font_size, 'normal'), )
map_field.config(insertbackground="White", borderwidth = 8, font=('Lucida Console', map_font_size, 'normal'))
scrollbar.config(command=text_field.yview)
textentry.config(insertbackground="White")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_propagate(False)


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def tag_yellow(word):
    """Highlight text (UNKNOWN COMMAND)."""
    pos = text_field.search(word, start, stopindex = END)
    pos_start = float(pos)
    pos_end = pos_start+0.17
    global start; start = pos_end
    text_field.tag_add('tag_green', pos_start, pos_end)
    text_field.tag_config('tag_green', background='White', foreground='Black', font=('Helvetica', 12, 'bold'))

def auto_setfocus(event):
    """Prevent clicking away from text entry."""
    textentry.focus_force()
    root.state('zoomed')

def toggle_fullscreen(event):
    global fs_var
    if (root.attributes('-fullscreen')):
        root.attributes('-fullscreen', False)
    else:
        root.attributes('-fullscreen', True)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def _start_0():
    '''First phase of start, entering world information.'''
    text_field.insert(END, '\nPlease enter world name:')
    global waiting_value; waiting_value = True

    print 'start sequence 0' #Debug msg

def _start_1():
    global started, pc_row, pc_col
    intro_story = """\n\
    \nWorld name: %s \
    \n<PLACE HOLDER TEXT> \
    """%(profile_name)

    text_field.insert(END, intro_story)

    print 'start sequence 1' #Debug msg
    started = True
    draw_map(pc_row, pc_col)


def _load_(): #----------------------------------> Needs an update.
    """Choose already existing yml file to set as profile_name."""
    pass

def save_state():
    #print 'func: Save state'
    pass #--------------------------- Load data into profile yml file
    #ymlr.enter_data('')
    root.after(1000, save_state)
root.after(1000, save_state) # Initiate save loop

def _quit_():
    root.quit()

class Bot:
    def __init__(self, namebot, hp, mp, loc):
        global profile_name, world_file
        self.botname = namebot
        self.health = hp
        self.energy = mp
        self.location = loc
        namebot = 'bot_' + self.botname # Bot tag in the front of the yaml elements.
        botinfo = {'health': self.health, 'energy': self.energy, 'loc': self.location}
        print namebot,',', botinfo,',', profile_name
        ymlr.enter_data(namebot, botinfo, world_file)

def create_bot(namebot, hp = default_hp, mp = default_mp, loc = default_loc):
    try : exists_ = ymlr.get_data('bot_' + namebot, world_file) # Check if bot exists in yaml file.
    except :
        bots[namebot] = Bot(namebot, hp, mp, loc)
        str_bot = "\n►[ ID: %s | HP: %d | MP: %d | LOC: %s ]" %(bots[namebot].botname,
        bots[namebot].health , bots[namebot].energy ,bots[namebot].location) # Print bot stats in the bot_field.
        print str_bot
        bot_field.insert(END, str_bot)

def enterpressed(event):
    """Get input from text entry when Enter(return) is pressed and delete the previous text."""
    userinput = textentry.get()
    text_field.insert(END, '\n>') #----------Echo
    text_field.insert(END, userinput) #----------Echo
    text_field.update()
    textentry.delete(0, END)

    global waiting_value, name_entered, last_input, real_input, real_parsed
    if waiting_value == False:
        real_input = userinput
        real_parsed = real_input.split(' ')
        userinput = userinput.lower()
        if userinput != '':
            try_execute_command(userinput)
            last_input = userinput
    else: #------------------------------------> Program is waiting for a value.
        parsing = userinput
        parsing = parsing.split(' ')
        if parsing[0] != '': #-----------If it's not empty.
            if name_entered == False:
                setup_world(userinput) # Setup a new world
                waiting_value = False
    text_field.see('end') #---------------Autoscroll down
    print '>>', userinput #Debug

def setup_world(_input): # CREATE NEW WORLD, FILE NAME == WORLD NAME
    '''User is in the setting up stages and havent entered world name yet.'''
    global profile_name, name_entered, waiting_value, world_file
    profile_name = _input + '.yml'
    print profile_name, '<-Profile name'
    _path = path.get_path()
    _path = _path + 'worlds\\' + profile_name
    print _path, '<-Path'
    world_file = _path # Set world_file as full location of the file
    world_yml = open(world_file , 'w+') #--Open if profile exists; create if not
    yml_info = {'world_name':_input}
    ymlr.insert(yml_info, world_file)
    name_entered = True
    waiting_value = False
    _start_1()

def get_last_input(event):
    """Re-enter last returned command into textentry."""
    global last_input
    textentry.insert(END, last_input)

def switch_bot(switch_to):
    global pc_row, pc_col, pc_name, world_file
    botname = 'bot_' + switch_to
    bot_data = ymlr.get_data(botname, world_file)
    parse_loc = tools.parse_str_loc(bot_data['loc'])
    pc_row = parse_loc[0]; pc_col = parse_loc[1]
    pc_row = int(pc_row); pc_col = int(pc_col)
    draw_map(pc_row, pc_col)
    print 'func: switch_bot, bot_data print ->',pc_row, pc_col , bot_data

def try_execute_command(userinput0):
    """Parse and execute entered command."""
    parsing = userinput0
    parsing = parsing.split(' ')

    print parsing #Debug

    if started == False:
        """If the game is in the title screen"""
        menu_commands = ['start', 'load', 'quit']
        legal_command = cmd.find_command(parsing[0], menu_commands)
        print legal_command

    else : legal_command = cmd.find_command(parsing[0])

    if legal_command == None:
        '''Error message.'''
        text_field.insert(END, '\n')
        text_field.insert(END, ' UNKNOWN COMMAND ')
        tag_yellow(' UNKNOWN COMMAND ')

    else: #Execute command
        if legal_command == 'create' and parsing[1] == 'bot':
            global real_parsed
            create_bot(real_parsed[2]) #----------------->Change

        if (legal_command == 'north' or legal_command == 'south'
        or legal_command == 'east' or legal_command == 'west'):
            mov_pc(legal_command)

        if legal_command == 'start': _start_0()
        if legal_command == 'load': _load_()
        if legal_command == 'quit': _quit_()

        if legal_command == 'control': switch_bot(parsing[1])

def mov_pc(_direction):
    """Relocate player/bot location based on given direction."""
    global pc_row, pc_col
    if _direction == 'north': pc_row -= 1
    if _direction == 'south': pc_row += 1
    if _direction == 'east': pc_col += 4
    if _direction == 'west': pc_col -= 4
    draw_map(pc_row, pc_col)

def draw_map(p_row, p_col):
    """Go through the nodes around the given coordinates."""
    global world_file, bot_avatar, np_bot_avatar
    map_field.delete(1.0, END) #  Clean the map field before writing.
    prnt_mainfeed(p_row, p_col) #  Print the standed node's information
    start_row = p_row-(map_height/2)
    start_col = p_col-(map_width/2)
    end_row = p_row+(map_height/2)+1
    end_col= p_col+(map_width/2)+1

    stream = open(world_file, 'r')
    profile = yaml.load(stream) # Player information is stored here.

    for cur_row in range(start_row, end_row):
        for cur_col in range(start_col, end_col, 4):
            bot_exists = False; pc_exists = False

            for bot_key in profile:
                if 'loc' in profile[bot_key]:
                    addr = tools.parse_str_loc(profile[bot_key]['loc'])
                    chkd_row = int(addr[0]); chkd_col = int(addr[1])
                    if chkd_row == cur_row and chkd_col == cur_col:
                            bot_exists = True
                    else: bot_exists = False

            if cur_row == p_row and cur_col == p_col: pc_exists = True
            else: pc_exists = False

            if pc_exists == True: map_field.insert(END, bot_avatar)

            else:
                if bot_exists == True:
                    map_field.insert(END, np_bot_avatar)
                else:
                    bot_exists = False
                    map_field.insert(END, botmap.node(cur_row, cur_col))
        map_field.insert(END, '\n')

def prnt_mainfeed(p_row, p_col):
    """Inserts the node-state text to the main feed."""
    _addr = '%d:%d'  %(p_row, p_col)
    envo_node = botmap.recog_node(_addr)
    npc_node = world.chcknode(_addr, 'NPC')
    adven_node = world.chcknode(_addr, 'ADVE')
    print npc_node
    if npc_node == 'None': npc_node = 'No one'
    if adven_node == 'None':adven_node = 'There is nothing here.'
    npc_idle = npc.call_npc(npc_node, 'idle')

    node_msg = "\n--------------------------------\
                \nYour coordinates: [%s] \
                \nRight now you are in %s \
                \n%s is here \
                \n%s \
                \n%s \
                \n--------------------------------"\
                %(_addr, envo_node, npc_node, npc_idle, adven_node)
    text_field.insert(END, node_msg)


#-------------------------------------------------------------------------------
#---------------------------Bind-Events-----------------------------------------
textentry.bind('<Return>', enterpressed)
textentry.bind('<Up>', get_last_input)
root.bind("<Button-1>", auto_setfocus)
root.bind("<F11>", toggle_fullscreen)
textentry.focus_force()

'''Program Start'''
text_field.insert(END, botter_title)
text_field.insert(END, entry_message)


'''Tests'''
setup_world('profile')
create_bot('testbot0', 100, 100, '9:48')
create_bot('testbot1', 100, 100, '11:44')
create_bot('testbot2', 100, 100, '12:48')

#-------------------------------------------------------------------------------
root.mainloop() #Gui Programs need a loop to stay on the screen.
