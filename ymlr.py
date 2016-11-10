import yaml
import path

def retrieve(filename = 'profile.yml'):
    _path = path.get_path(filename)
    with open(_path, 'r') as file_descriptor:
        yml_data = yaml.load(file_descriptor)
    return yml_data

def insert(data, filename = 'profile.yml' ):
    _path = path.get_path(filename)
    with open(_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file)

def enter_data(cont, valinput, filename = 'profile.yml'): #Cont for container
    yml_path = path.get_path(filename) #profile.yml
    stream = open(yml_path, 'r')
    prof = yaml.load(stream) # Player information is stored here.
    print prof
    prof[cont] = valinput
    with open(yml_path, 'w') as yaml_file:
        yaml_file.write(yaml.dump(prof, default_flow_style = False))

def get_data(cont, filename = 'profile.yml'):
    yml_path = path.get_path(filename) #profile.yml
    stream = open(yml_path, 'r')
    profile = yaml.load(stream) # Player information is stored here.
    return profile[cont]

print retrieve()
