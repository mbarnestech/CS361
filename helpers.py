import os
import pickle


def clear_terminal():
    os.system("clear||cls") # thanks reddit! found here: https://www.reddit.com/r/learnpython/comments/1b4sk5n/how_to_clear_a_console_in_python/


def pickle_obj(obj):
    name = obj.name.replace(' ', '_')
    file_path = "./lists/" + name + ".pickle"

    with open(file_path, 'wb') as file:
        file.dump(obj)

def unpickle_obj(list_name):
    name = list_name.replace(' ', '_')
    file_path = "./lists/" + name + ".pickle"

    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'wb') as file:
        obj = file.load()
    
    return obj