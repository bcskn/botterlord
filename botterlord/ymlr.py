import yaml, tools

#def retrieve(filename):
#    with open(filename, 'r') as file_descriptor:
#        yml_data = yaml.load(file_descriptor)
#    return yml_data
def retrieve(cont, filename):
    stream = file(filename, 'r')
    data = yaml.load(stream)
    #return yaml.dump(data, encoding=('utf-8'), default_flow_style=False, allow_unicode=True)
    return data[cont].encode('utf-8')

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
    data = yaml.dump(profile, default_flow_style = False, encoding=('utf-8'))
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

def write_to_world(data, profile):
    pass

def create_world(input_):
    new_file_loc = "botterlord/worlds/%s"%(input_+'.yml')
    print "New file will be created at %s"%(new_file_loc)
    new_file_loc = tools.get_path(new_file_loc)
    dump_data = { \
    'name': input_, \
    'level': None \
    }
    with open(new_file_loc, 'w+') as new_profile:
        yaml.dump((dump_data), new_profile, default_flow_style=False)
        print "File created."

    print "Start command entered with input following: <'%s'>"%(input_)
    pass # Start a world with returned[1]
