# -*- coding: utf-8 -*-
import os, sys, sqlite3, yaml, platform # Dependencies
from Tkinter import *
from screeninfo import get_monitors
#-----------------------
import cmd, world, npc, ymlr, tools
from texts import status

#----------------------------------------------DISPLAY SETTINGS
topbar_name = 'BotterLord DEV Version'
icon_name = 'Botter_logo.ico'  # Icon must be in .ico format.

screen_size = tools.get_monitor_size()
print "Monitor Resolution: %s "%(screen_size)

default_cursor_style = "dotbox"

map_frame_height = screen_size["height"] #475
bot_frame_height = screen_size["height"]/6#475
bot_frame_width = screen_size["width"]/2.5 #900 # Also the map is bound to this tile thus == map_frame_width

window_minimum_height = screen_size["height"]/3
window_minimum_width = screen_size["width"]/3
window_background_color = 'gray50'

map_font = 'Lucida Console'
main_font = 'Lucida Console'
bot_font = 'Lucida Console'

map_font_size = 13
bot_font_size = 15
main_font_size = 10

#----------------------------------------------DEFAULT INGAME VALUES
default_hp = 100
default_mp = 100
default_loc = '10:44'
#----------------------------------------------




'''------Get Images------'''
_icon_path = os.path.join(tools.get_path(),'images',icon_name) # Retrieve image from images folder.

'''-----Connect to the Database-----'''
conn = sqlite3.connect(os.path.join('data','botterlord.db'))
db = conn.cursor()

'''-----Variables-----'''
start = 1.0 #Start Line
fs_var = 0 #Fullscreen state
real_input = ''
real_parsed = ''
bot_locs = []

'''----- Variables stored in profile (yaml) file-----'''
world_file = ''
profile_name = '' # Loaded profile file and world name
bots = {}
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

try: root.iconbitmap(_icon_path) #Window icon
except: print "Can't get icon because of unknown reasons."
root.minsize(window_minimum_width, window_minimum_height)
root.configure(background=window_background_color)

print platform.system()
if platform.system() == "Windows":
    if root.state('zoomed') == False:
        root.state('zoomed')

else: root.attributes('-fullscreen', True) # If not windows automatically switch to fullscreen


#Relief is for widget "style"
map_frame = Frame(root,bg = "Black",relief=FLAT, height=map_frame_height)
bot_frame = Frame(root,bg = "Black",relief=FLAT, height=bot_frame_height, width=bot_frame_width)
text_field = Text(root,bg = "Black", fg="White",relief=FLAT)
bot_field = Text(bot_frame,bg = "Black", fg="White",relief=FLAT)
map_field = Text(map_frame,bg = "Black", fg="White",relief=FLAT)
textentry = Entry(root, bg = "Black", fg = "White", relief=FLAT)
scrollbar = Scrollbar(root, bg = "Black", relief=FLAT)

map_frame.grid(row=1, column=1, sticky=W+E+N+S, cursor=None)
bot_frame.grid(row=0, column=1, sticky=W+E+N+S, pady=(8,8))
map_frame.grid_propagate(False)
bot_frame.grid_propagate(False)
text_field.grid(row=0,column=0,rowspan=2,sticky=W+E+N+S, padx = (8, 8), pady = (8, 0))
bot_field.grid(sticky=W+E+N+S)
map_field.grid(sticky=W+E+N+S)
textentry.grid(row=2,column=0,columnspan=3,sticky=E+W, padx = 8, pady = 8)
scrollbar.grid(row=0,column=2,rowspan=2, sticky=E+N+S, padx=(8,8), pady=(8,0))

text_field.config(insertbackground="White",yscrollcommand=scrollbar.set, borderwidth = 10, \
font=(main_font, main_font_size, 'normal'))
bot_field.config(insertbackground="White", borderwidth = 10, font=(bot_font, bot_font_size, 'normal'))
map_field.config(insertbackground="White", borderwidth = 8, font=(map_font, map_font_size, 'normal'))
scrollbar.config(command=text_field.yview)
textentry.config(insertbackground="White")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_propagate(False)


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def cursor_style(style):
    text_field.config(cursor=style)
    bot_field.config(cursor=style)
    map_field.config(cursor=style)
    scrollbar.config(cursor=style)
    textentry.config(cursor=style)
    root.config(cursor=style)


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

def scale_font_size():
    print text_field.winfo_width()
    global main_font_size, botter_title
    pixel_ratio = 0.01
    main_font_size = int(text_field.winfo_width()*pixel_ratio) + \
    (text_field.winfo_width() % pixel_ratio > 0)
    print main_font_size
    text_field.config(font=('Lucida Console', main_font_size, 'normal'))
    botter_title = tools.fit_title(root.winfo_screenwidth()) # Won't work because title is already printed


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


def _load_():
    """Choose already existing yml file to set as profile_name."""
    pass

def save_state():
    #print 'func: Save state'
    pass #--------------------------- Load data into profile yml file
    #ymlr.enter_data('')
    root.after(1000, save_state)
root.after(1000, save_state) # Initiate save loop

class Bot:
    def __init__(self, namebot, hp, mp, loc):
        global profile_name, world_file
        self.botname = namebot
        self.health = hp
        self.energy = mp
        self.location = loc
        namebot = 'bot_' + self.botname # Bot tag in the front of the yaml elements.
        botinfo = {'health': self.health, 'energy': self.energy, 'location': self.location}
        print namebot,',', botinfo,',', profile_name
        ymlr.enter_data(namebot, botinfo, world_file)

def update_botfield():
    """Get data from worldfile on player bots and update bot_field display."""
    #Changeable order.
    global world_file; prof = yaml.load(open(world_file, 'r')) #Only read it.
    for key in prof:
        if key.startswith("bot_") == True:
            str_bot = "\n►[ ID: %s | HP: %d | MP: %d | LOC: %s ]" %(key, prof[key]["health"],
            prof[key]["energy"], prof[key]["location"])
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
    world_file = os.path.join(tools.get_path(),'worlds',profile_name)
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
    """Control another Bot."""
    global pc_row, pc_col, pc_name, world_file
    ymlr.internal_data(world_file, 'in', "%d:%d"%(pc_row, pc_col), pc_name, 'location')

    botname = 'bot_' + switch_to
    bot_data = ymlr.get_data(botname, world_file)
    parse_loc = tools.parse_str_loc(bot_data['loc'])
    pc_row = parse_loc[0]; pc_col = parse_loc[1]
    pc_row = int(pc_row); pc_col = int(pc_col)
    pc_name = botname
    print "printing >> switch_bot > pc_row, pc_col, bot_data:   ",pc_row, pc_col , bot_data

def try_execute_command(userinput0):
    """Parse and execute entered command."""
    parsing = userinput0
    parsing = parsing.split(' ')

    print "printing >> try_execute_command > parsing:   ", parsing

    if started == False:
        """If the game is in the title screen"""
        menu_commands = ['start', 'load', 'quit']
        legal_command = cmd.find_command(parsing[0], menu_commands)
        print "printing >> try_execute_command > legal_command:  ",legal_command # Track message

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
        if legal_command == 'quit': root.quit()
        if legal_command == 'control': switch_bot(parsing[1])
        if legal_command == 'show_mouse': cursor_style("dotbox") #Default
        if legal_command == 'hide_mouse': cursor_style("none")
        if legal_command == 'status': pass # Show current status
        if legal_command == 'help': help_show()

def mov_pc(_direction):
    """Relocate player/bot location based on given direction."""
    global pc_row, pc_col
    if _direction == 'north': pc_row -= 1
    if _direction == 'south': pc_row += 1
    if _direction == 'east': pc_col += 4
    if _direction == 'west': pc_col -= 4


def prnt_mainfeed(p_row, p_col):
    """Inserts the node-state text to the main feed."""
    _addr = '%d:%d'  %(p_row, p_col)
    npc_node = world.chcknode(_addr, 'NPC')
    adven_node = world.chcknode(_addr, 'ADVE')
    print "printing >> prnt_mainfeed, npc_node:  ", npc_node # Track message
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
                %(_addr, npc_node, npc_idle, adven_node)
    text_field.insert(END, node_msg)

def help_show():
    cmds = "\n%s"%(cmd.pc_commands)
    text_field.insert(END, cmds)


#-------------------------------------------------------------------------------
#---------------------------Bind-Events-----------------------------------------
textentry.bind('<Return>', enterpressed)
textentry.bind('<Up>', get_last_input)
root.bind("<Button-1>", auto_setfocus)
root.bind("<F11>", toggle_fullscreen)
textentry.focus_force()

cursor_style(default_cursor_style)

'''Program Start'''
text_field.insert(END, botter_title)
text_field.insert(END, entry_message)


'''Tests'''
setup_world('profile')
world.store_bot_location(world_file)
root.after(500, scale_font_size) # Needs time
#switch_bot("testbot2")
update_botfield()
#-------------------------------------------------------------------------------
root.mainloop() #Gui Programs need a loop to stay on the screen.
