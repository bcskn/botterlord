'''Command Space and Parsing'''
pc_commands = ['start', 'load', 'quit', 'create', 'set', 'north', 'east', 'west', 'south', 'control']
admin_commands = []

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
