# -*- coding: utf-8 -*-
import os, sys, yaml, platform # Dependencies -sqlite3
from Tkinter import *
from screeninfo import get_monitors
#-----------------------
import cmd, ymlr, tools

#Note: This script is mostly just a trigger script. Can't test it much.
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
window_background_color = 'white' #gray50

map_font = 'Courier New'
main_font = 'Courier New'
bot_font = 'Courier New'

map_font_size = 13
bot_font_size = 13
main_font_size = 9

pad_width = 3

#----------------------------------------------DEFAULT INGAME VALUES
default_hp = 100
default_mp = 100
default_loc = '10:44'
#----------------------------------------------


'''------Get Images------'''
_icon_path = tools.get_path("images/botter_logo.ico") # Retrieve image from images folder.

'''-----Variables-----'''
global start
start = 1.0 #Start Line
fs_var = 0 #Fullscreen state
input_log = []
bot_locs = []

#tools.get_path path for texts.yml works on runscript package for atom
#but it doesn't work with cmd python command on windows 10, didn't test on
#different operating systems.
texts_path = tools.get_path("texts/texts.yml")
try:
    retrieved = ymlr.retrieve('title', texts_path)
except:
    retrieved = ymlr.retrieve('title', texts_path)
print "banner: \n", retrieved

#---------------------------------------------
started = False #In title screen
waiting_value = False
name_entered = False

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

main_frame.grid(row=0,column=0,rowspan=2,sticky=W+E+N+S, padx = (pad_width, pad_width), pady = (pad_width, 0))
bot_frame.grid(row=0, column=1, sticky=W+E+N+S, pady=(pad_width,pad_width), padx=(0,pad_width))
map_frame.grid(row=1, column=1, sticky=W+E+N+S, cursor=None, padx=(0,pad_width))
main_frame.grid_propagate(False)
map_frame.grid_propagate(False)
bot_frame.grid_propagate(False)

text_field = Text(main_frame,bg = "Black", fg="White",relief=FLAT)
bot_field = Text(bot_frame,bg = "Black", fg="White",relief=FLAT)
map_field = Text(map_frame,bg = "Black", fg="White",relief=FLAT)
textentry = Entry(root, bg = "Black", fg = "White", relief=FLAT)

text_field.pack(fill=BOTH, expand=1)
bot_field.place(rely=0, relx=0,relwidth=1, relheight=1, anchor=NW)
map_field.place(rely=0, relx=0,relwidth=1, relheight=1, anchor=NW)


textentry.grid(row=2,column=0,columnspan=3,sticky=E+W, padx = pad_width, pady = pad_width)

text_field.config(insertbackground="White", wrap=WORD, borderwidth = 10, \
font=(main_font, main_font_size, 'normal'))
bot_field.config(insertbackground="White", borderwidth = 8, font=(bot_font, bot_font_size, 'normal'))
map_field.config(insertbackground="White", borderwidth = 8, font=(map_font, map_font_size, 'normal'))
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

    def start_message(self):
        text_field.insert(END, ymlr.retrieve('start_message', texts_path))

    def load_message(self):
        text_field.insert(END, "\nLOAD MESSAGE PLACEHOLDER")
        pass # Do the loading here.

    def quit_question(self):
        text_field.insert(END, "\nAre you sure you want to quit ?")
        pass # Doesn't really have anything left to do, all the quitting will be done
        # in the try_execute_command section when the last input is quit.

def start_phase(profilename):
    ymlr.create_world(profilename) # Randomized maybe ?
    #LOAD THE DATA FROM THE YAML FILE


def _load_(): #UNDER CONSTRUCTION
    """Choose already existing yml file to set as profile_name."""
    pass

def save_state(): #UNDER CONSTRUCTION
    #print 'func: Save state'
    pass #--------------------------- Load data into profile yml file
    #ymlr.enter_data('')
    root.after(1000, save_state)

def enterpressed(event):
    """Get input from text entry when Enter(return) is pressed and delete the previous text."""
    userinput = textentry.get()
    text_field.insert(END, '\n>') #----------Echo
    text_field.insert(END, userinput) #----------Echo
    text_field.update()
    textentry.delete(0, END) #Clear the text entry field.

    global input_log, real_input, real_parsed
    userinput = userinput.lower()
    real_parsed = userinput.split(' ') #Split the input into tokens, globally accessible list
    if real_parsed[0] != '': #If returned text is not empty.
        input_log.append(userinput) # Store input on log
        print input_log
        try_execute_command(real_parsed) # Try to execute the first word on the input.


    text_field.see('end') #---------------Autoscroll down
    print '>>', userinput #Debug

def get_input_log():
    """Re-enter last returned command into textentry."""
    global input_log
    textentry.insert(END, input_log)

def try_execute_command(returned):
    global input_log
    """Parse and execute entered command. Trigger function."""

    print "(f)try_execute_command: ", returned
    legal_command = cmd.find_command(returned[0])
    print legal_command

    previous_item = cmd.previous_command(input_log) # Test this

    if legal_command == None:
        print input_log
        #If there is no such command but still check for previous command relation.
        #If not related, print tagged error message.

        if previous_item == 'start':
            start_phase(returned[0])


        elif previous_item == 'load':
            print "Load command entered."
            pass # Start a world with returned[1]

        elif previous_item == 'quit':
            # Quit game if returned[1] is yes, or don't do anything if it was no or else.
            if returned[0] == 'yes':
                root.quit()
            else:
                pass # Don't do anything.

        else: #No previous command relation print error message.
            '''Error message.'''
            text_field.insert(END, '\n')
            text_field.insert(END, ' UNKNOWN COMMAND ')
            print "UNKNOWN COMMAND"
            tag_yellow(' UNKNOWN COMMAND ')

    else: #----------------Found legal command, try executing it.

        if legal_command == 'create' and parsing[1] == 'bot':
            global real_parsed
            create_bot(real_parsed[2]) #----------------->Change

        if legal_command == 'start': start_screen.start_message() # Start message
        if legal_command == 'load': start_screen.load_message() # Load message
        if legal_command == 'quit': start_screen.quit_question() # Quit question

        if legal_command == 'control': switch_bot(parsing[1])
        if legal_command == 'show_mouse': cursor_style("dotbox") #Default
        if legal_command == 'hide_mouse': cursor_style("none")
        if legal_command == 'status': pass # Show current status
        if legal_command == 'help': help_show()
        if legal_command == 'log': get_input_log()
    return True #No crash

def help_show():
    cmds = "\n%s"%(cmd.pc_commands)
    text_field.insert(END, cmds)

def get_last(event):
    global input_log
    try:
        last_ = len(input_log) - 1
    except:
        pass # No input recorded in the log yet.
    stringer = '\n' + str(input_log[last_])
    textentry.insert(END, stringer)


#-------------------------------------------------------------------------------
#---------------------------Bind-Events-----------------------------------------
textentry.bind('<Return>', enterpressed)
textentry.bind('<Up>', get_last)
root.bind("<Button-1>", auto_setfocus)
root.bind("<F11>", toggle_fullscreen)
root.after(1000, save_state) # Initiate save loop
textentry.focus_force()

cursor_style(default_cursor_style)

'''Program Start'''
start_screen = main_menu(retrieved, entry_message)
start_screen._print()


'''Tests'''

"""
Tests:
try_execute_command("start")

"""
test_text = ymlr.retrieve('test_text', texts_path)
bot_field.insert(END, test_text)
map_field.insert(END, test_text)
text_field.insert(END, test_text)


#-------------------------------------------------------------------------------
root.mainloop() #Gui Programs need a loop to stay on the screen.
