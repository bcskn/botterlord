'''Command Space and Parsing'''
pc_commands = ['start', 'load', 'quit', 'create', 'set', 'north', 'east', 'west', 'south', 'control',
'show_mouse', 'hide_mouse', "status", 'help', 'log']
admin_commands = []

def previous_command(input_):
    if len(input_) != 0:
        previous_item = len(input_) - 2 # -1 because list index starts from 0 and -1 to go to the previous input.
        print "length of input log:", len(input_)
        print "last item:", previous_item
        return input_[previous_item]
    else: # List is empty.
        return None

def find_command(string, allowed_commands=None):
    """Match user command with known commands."""
    if allowed_commands is None:    #  Available commands to the user
        allowed_commands = pc_commands

    matching_commands = []

    for command in allowed_commands:
        if command.startswith(string):
            matching_commands.append(command)

    if len(matching_commands)==1:
        #There is a match
        return matching_commands[0]     #  Return matched command input

    return None     #  If there is no match
