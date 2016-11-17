import yaml
import path

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
    print prof
    prof[cont] = valinput
    with open(filename, 'w') as yaml_file:
        yaml_file.write(yaml.dump(prof, default_flow_style = False))

def get_data(cont, filename):
    stream = open(filename, 'r')
    profile = yaml.load(stream) # Player information is stored here.
    return profile[cont]
