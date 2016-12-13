import yaml, tools

def retrieve(filename):
    with open(filename, 'r') as file_descriptor:
        yml_data = yaml.load(file_descriptor)
    return yml_data

def insert(data, filename):
    with open(filename, 'w') as yaml_file:
        yaml.dump(data, yaml_file)

def enter_data(cont, valinput, filename): #Cont for container#profile.yml
    stream = open(filename, 'r')
    prof = yaml.load(stream) # Player information is stored here.
    prof[cont] = valinput
    with open(filename, 'w') as yaml_file:
        yaml_file.write(yaml.dump(prof, default_flow_style = False))

def get_data(cont, filename):
    stream = open(filename, 'r')
    profile = yaml.load(stream) # Player information is stored here.
    return profile[cont]

def internal_data(filename, io, entry, cont, cont_in = None, cont_in2 = None): #Supports up to 3 containers stacked on top.
    "filename = 'string',, io = [in, out],, entry = val,, cont,,..."
    stream = open(filename, 'r')
    prof = yaml.load(stream)
    if io == 'out':
        if cont_in == None:
            val = prof[cont]
        else:
            if cont_in2 == None:
                val = prof[cont][cont_in]
            else:
                val = prof[cont][cont_in][cont_in2]
        return val

    if io == 'in':
        if cont_in == None:
            prof[cont] = entry
        else:
            if cont_in2 == None:
                prof[cont][cont_in] = entry
            else:
                prof[cont][cont_in][cont_in2] = entry
        with open(filename, 'w') as yaml_file:
            yaml_file.write(yaml.dump(prof, default_flow_style = False))
