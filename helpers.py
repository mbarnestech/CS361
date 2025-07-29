import os
import pickle
import sys

# --------- terminal / system helpers -------------
def clear_terminal():
    """
    clears the terminal for a less chaotic user experience
    """
    os.system("clear||cls") # thanks reddit! found here: https://www.reddit.com/r/learnpython/comments/1b4sk5n/how_to_clear_a_console_in_python/

def exit_program():
    """
    exits the program with a code of 0 (success)
    """
    sys.exit(0)

# --------- in-service file storage helpers -------------
def pickle_obj(obj):
    """
    takes a python object and saves it as a pickled file
    """
    name = obj.name.replace(' ', '_')
    file_path = "./" + name + ".pickle"

    with open(file_path, 'wb') as file:
        pickle.dump(obj, file)

def unpickle_obj(list_name):
    """
    takes a pickled file for a particular list name
    and returns the unpickled python object
    """
    name = list_name.replace(' ', '_')
    file_path = "./" + name + ".pickle"

    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'rb') as file:
        obj = pickle.load(file)
    
    return obj

# --------- pages helpers -------------
def get_option_num(options, input_text):
    """
    prints list of options, validates user option choice, returns choice
    """
    print("")
    for i in range(len(options)):
        print(f"{i+1}. {options[i][0]}")
    print("")

    # Get user input
    option = input(input_text)
    while option not in [str(num + 1) for num in range(len(options))]:
        print(f"I'm sorry, \"{option}\" is not a valid choice. Please try again.")
        option = input(input_text)
    
    return option

def print_current_list(current):
    """
    prints information on current list
    """
    print(f"Your current To-Do List is {current.name} and is owned by {current.owner}.")
    print("")


def is_float(time):
    """
    returns whether string input can be translated to a floating point number
    """
    # credit for this entire function - https://www.geeksforgeeks.org/python/how-to-check-if-a-string-can-be-converted-to-float-in-python/#
    try:
        float(time)
        return True
    except ValueError:
        return False
    