from to_do_list import Task, ToDoList, Lists
import zmq
import os
import helpers
from dotenv import load_dotenv

def welcome():
    helpers.clear_terminal()
    lists = helpers.unpickle_obj("List of Lists")
    if not lists:
        lists = Lists()
    if lists.is_empty():
        first = ToDoList("My First List")
        lists.add_list(first)
    default = lists.lists["universal"][0]
    print("Hi! Welcome to the To-Do List App.")
    print("")
    print("This app will help your productivity by allowing you to import, create, edit, and organize your to-do list. It will even help you prioritize your list to fit the time you have!")
    print("")
    _ = input("Press 'return' to continue: ")
    return default, lists

def options():
    pass

if __name__ == "__main__":
    current_list, list_of_lists = welcome()
    print(current_list)

