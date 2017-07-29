# -*- coding: utf-8 -*-
import os, sys, yaml, platform # Dependencies -sqlite3
from Tkinter import *
from screeninfo import get_monitors
#-----------------------
import cmd, ymlr, tools

#----------------------------------------------DISPLAY SETTINGS
version_number = "Alpha0.1"
topbar_name = 'BotterLord'
icon_name = 'Botter_logo.ico'  # Icon must be in .ico format.

screen_size = tools.get_monitor_size()
print "Monitor Resolution: %s "%(screen_size)

default_cursor_style = "dotbox"

map_frame_height = screen_size["height"]/6 #475
bot_frame_height = screen_size["height"]/6 #475
side_frame_width = screen_size["width"]/3 #900 # Also the map is bound to this tile thus == map_frame_width

window_minimum_height = screen_size["height"]/3
window_minimum_width = screen_size["width"]/3
window_background_color = 'gray50'

map_font = 'Courier New'
main_font = 'Courier New'
bot_font = 'Courier New'

map_font_size = 13
bot_font_size = 13
main_font_size = 9

#----------------------------------------------DEFAULT INGAME VALUES
default_hp = 100
default_mp = 100
default_loc = '10:44'
#----------------------------------------------


'''------Get Images------'''
_icon_path = tools.get_path("images/botter_logo.ico") # Retrieve image from images folder.

'''-----Connect to the Database-----'''
#conn = sqlite3.connect(os.path.join('data','botterlord.db'))
#db = conn.cursor()

'''-----Variables-----'''
global start
start = 1.0 #Start Line
fs_var = 0 #Fullscreen state
real_input = ''
real_parsed = ''
bot_locs = []

#tools.get_path path for texts.yml works on runscript package for atom
#but it doesn't work with cmd python command on windows 10, didn't test on
#different operating systems.
title_path = tools.get_path("texts/texts.yml")
try:
    retrieved = ymlr.retrieve(title_path)
except:
    retrieved = ymlr.retrieve(title_path)
print retrieved

#---------------------------------------------
started = False #In title screen
waiting_value = False
name_entered = False
last_input = '' # The last entered command

entry_message = """\
\n Welcome to BotterLord %s \
\n                  \
\n Insert a command \
\n --------------- \
\n Start\
\n Load\
\n Quit\
\n --------------- \
"""%(version_number)
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
'''----------------Window Setup----------------'''

root = Tk() #Main Frame
root.title(topbar_name)

try: root.iconbitmap(_icon_path) #Window icon
except: print "Can't get icon because of unknown reasons."
root.minsize(window_minimum_width, window_minimum_height)
root.configure(background=window_background_color)

print "Operating System: ", platform.system()
if platform.system() == "Windows":
    if root.state('zoomed') == False:
        root.state('zoomed')

else: root.attributes('-fullscreen', True) # If not windows automatically switch to fullscreen


#Relief is for widget "style"
main_frame = Frame(root,bg = "Black",relief=FLAT)
bot_frame = Frame(root,bg = "Black",relief=FLAT, height=bot_frame_height, width=side_frame_width)
map_frame = Frame(root,bg = "Black",relief=FLAT, height=map_frame_height, width=side_frame_width)

main_frame.grid(row=0,column=0,rowspan=2,sticky=W+E+N+S, padx = (8, 8), pady = (8, 0))
bot_frame.grid(row=0, column=1, sticky=W+E+N+S, pady=(8,8))
map_frame.grid(row=1, column=1, sticky=W+E+N+S, cursor=None)
main_frame.grid_propagate(False)
map_frame.grid_propagate(False)
bot_frame.grid_propagate(False)

text_field = Text(main_frame,bg = "Black", fg="White",relief=FLAT)
bot_field = Text(bot_frame,bg = "Black", fg="White",relief=FLAT)
map_field = Text(map_frame,bg = "Black", fg="White",relief=FLAT)
textentry = Entry(root, bg = "Black", fg = "White", relief=FLAT)
scrollbar = Scrollbar(root, bg = "Black", relief=FLAT)

text_field.pack(fill=BOTH, expand=1)
bot_field.place(rely=0, relx=0,relwidth=1, relheight=1, anchor=NW)
map_field.place(rely=0, relx=0,relwidth=1, relheight=1, anchor=NW)


textentry.grid(row=2,column=0,columnspan=3,sticky=E+W, padx = 8, pady = 8)
scrollbar.grid(row=0,column=2,rowspan=2, sticky=E+N+S, padx=(8,8), pady=(8,0))

text_field.config(insertbackground="White",yscrollcommand=scrollbar.set, wrap=WORD, borderwidth = 10, \
font=(main_font, main_font_size, 'normal'))
bot_field.config(insertbackground="White", borderwidth = 8, font=(bot_font, bot_font_size, 'normal'))
map_field.config(insertbackground="White", borderwidth = 8, font=(map_font, map_font_size, 'normal'))
scrollbar.config(command=text_field.yview)
textentry.config(insertbackground="White")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


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
    global start;
    pos = text_field.search(word, start, stopindex = END)
    pos_start = float(pos)
    pos_end = pos_start+0.17
    start = pos_end
    text_field.tag_add('tag_green', pos_start, pos_end)
    text_field.tag_config('tag_green', background='White', foreground='Black', \
    font=(main_font,main_font_size,'bold'))

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
    global main_font_size
    pixel_ratio = 0.01
    main_font_size = int(text_field.winfo_width()*pixel_ratio) + \
    (text_field.winfo_width() % pixel_ratio > 0)
    print main_font_size
    text_field.config(font=('Lucida Console', main_font_size, 'normal'))



#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class main_menu:
    def __init__(self, title, menu_text):
        self.title = title
        self.menu_text = menu_text

    def _print(self):
        text_field.delete((0.0), END)
        text_field.insert(END, self.title)
        text_field.insert(END, self.menu_text)

    def _start(self):
        text_field.insert(END, "\nSTART MESSAGE") #How to wait for a value the right way ?


def _load_(): #UNDER CONSTRUCTION
    """Choose already existing yml file to set as profile_name."""
    pass

def save_state(): #UNDER CONSTRUCTION
    #print 'func: Save state'
    pass #--------------------------- Load data into profile yml file
    #ymlr.enter_data('')
    root.after(1000, save_state)

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
    textentry.delete(0, END) #Clear the text entry field.

    global last_input, real_input, real_parsed
    real_input = userinput
    real_parsed = real_input.split(' ')
    userinput = userinput.lower()
    if userinput != '':
        try_execute_command(userinput)
        last_input = userinput

    text_field.see('end') #---------------Autoscroll down
    print '>>', userinput #Debug

def setup_world(_input): # OBSOLETE --- REFACTOR
    '''User is in the setting up stages and havent entered world name yet.'''
    global profile_name, name_entered, waiting_value, world_file

    if _input != '': #-----------If it's not empty.
        if name_entered == False:
            profile_name = _input + '.yml'
            print "Profile Name: ", profile_name
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

def try_execute_command(userinput0):
    """Parse and execute entered command."""
    parsing = userinput0
    parsing = parsing.split(' ')

    print "(f)try_execute_command: ", parsing

    if started == True:
        """If the game is in the title screen"""
        menu_commands = ['start', 'load', 'quit']
        legal_command = cmd.find_command(parsing[0], menu_commands)
        print "printing >> try_execute_command > legal_command:  ",legal_command # Track message

    else : legal_command = cmd.find_command(parsing[0])

    if legal_command == None:
        '''Error message.'''
        text_field.insert(END, '\n')
        text_field.insert(END, ' UNKNOWN COMMAND ')
        print "UNKNOWN COMMAND"
        tag_yellow(' UNKNOWN COMMAND ')

    else: #--------------------------------------------------EXECUTE COMMAND
        if legal_command == 'create' and parsing[1] == 'bot':
            global real_parsed
            create_bot(real_parsed[2]) #----------------->Change

        if legal_command == 'start': start_screen._start()
        if legal_command == 'load': _load_()
        if legal_command == 'quit': root.quit()
        if legal_command == 'control': switch_bot(parsing[1])
        if legal_command == 'show_mouse': cursor_style("dotbox") #Default
        if legal_command == 'hide_mouse': cursor_style("none")
        if legal_command == 'status': pass # Show current status
        if legal_command == 'help': help_show()

def prnt_mainfeed(p_row, p_col): #------------OBSOLETE
    """Inserts the node-state text to the main feed."""
    pass
    """
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
"""
def help_show():
    cmds = "\n%s"%(cmd.pc_commands)
    text_field.insert(END, cmds)


#-------------------------------------------------------------------------------
#---------------------------Bind-Events-----------------------------------------
textentry.bind('<Return>', enterpressed)
textentry.bind('<Up>', get_last_input)
root.bind("<Button-1>", auto_setfocus)
root.bind("<F11>", toggle_fullscreen)
root.after(1000, save_state) # Initiate save loop
textentry.focus_force()

cursor_style(default_cursor_style)

'''Program Start'''
start_screen = main_menu(retrieved, entry_message)
start_screen._print()


'''Tests'''
test_text = """\
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ
KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK
LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
"""
bot_field.insert(END, test_text)
map_field.insert(END, test_text)
text_field.insert(END, test_text)


#-------------------------------------------------------------------------------
root.mainloop() #Gui Programs need a loop to stay on the screen.
