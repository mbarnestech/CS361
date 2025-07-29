from to_do_list import Lists, ToDoList, Task
import helpers
import imports

def welcome_page():
    """
    Entry point into the program.
    """
    helpers.clear_terminal()
    lists = helpers.unpickle_obj("List of Lists")
    if not lists:
        lists = Lists()
    print("Hi! Welcome to the To-Do List App.")
    print("")
    print("This app will help your productivity by allowing you to import, create, edit, and organize your to-do list. It will even help you prioritize your list to fit the time you have!")
    print("")
    _ = input("Press 'return' to continue: ")
    options_page(lists)

def add_item_page(lists):
    """
    Provides UI to add a task to the active list
    """
    helpers.clear_terminal()
    helpers.print_current_list(lists.active)
    name = input("What is the name of the task? ")
    value = input("What is the value of the task (scale of 1-10): ")
    while value not in [str(num) for num in range(1,11)]:
        print("The value must be a number between 1 and 10 (inclusive).")
        value = input("What is the value of the task (scale of 1-10): ")
    time = input("How many hours do you estimate this task will take (decimals accepted)? ")
    while not helpers.is_float(time) or float(time) <= 0:
        print("The value must be a positive integer or decimal.")
        time = input("How many hours do you estimate this task will take (decimals accepted)? ")
    print("")
    print(f"The new task is named {name}, has a value of {value}, and is estimated to take {time} hours.")
    print("")
    print("1. Save the task.")
    print("2. Clear and start add item process over.")
    print("3. Clear and go back to options page.")
    print("4. Exit Program.")
    print("")
    option = input("Enter the number representing your choice: ")
    while option not in [str(num + 1) for num in range(4)]:
        print(f"I'm sorry, \"{option}\" is not a valid choice. Please try again.")
        option = input("Enter the number representing your choice: ")
    match option:
        case "1":
            new_task = Task(name, value, time)
            lists.active.add_task(new_task)
            print(f"Congratulations, you have added {name} to the list.")
            _ = input("Press 'return' to continue: ")
            options_page(lists)
        case "2":
            add_item_page(lists)
        case "3":
            options_page(lists)
        case "4":
            exit_page(lists)

def edit_item_page(lists):
    """
    Provides UI to edit a task on the active list
    """
    helpers.clear_terminal()
    helpers.print_current_list(lists.active)
    

    pass

def clear_list_page(lists):
    """
    Provides UI to clear the active list of all tasks
    """
    helpers.clear_terminal()
    helpers.print_current_list(lists.active)

    print(f"Are you sure you want to clear {lists.active.name}? This can only be undone until your next deletion action.")
    answer = input("Do you wish to proceed (y/n)? ")
    while answer not in ["y","n"]:
        print("invalid response, please enter 'y' or 'n'.")
        answer = input("Do you wish to proceed (y/n)? ")
    if answer == "y":
        lists.active.clear_list()
        print("List has been cleared.\n")
    _ = input("Press 'return' to continue: ")
    options_page(lists)
    

def view_list_page(lists):
    """
    Provides UI to view the active list
    """
    helpers.clear_terminal()
    helpers.print_current_list(lists.active)
    if lists.active.is_empty():
        print("This list is currently empty.")
    else:
        for i in range(len(lists.active.tasks)):
            print(f"{i+1}. {lists.active.tasks[i]}")
    print("")
    _ = input("Press 'return' to continue: ")
    options_page(lists)

def choose_existing_list_page(lists):
    """
    Provides UI to choose a new active list from existing list of lists
    """
    helpers.clear_terminal()
    helpers.print_current_list(lists.active)
    list_dict = lists.get_lists_for_user()
    for key, value in list_dict.items():
        print(f"{str(key)}. {value.name}")
    list = input("Which list would you like to make active? ")
    while list not in [str(num + 1) for num in range(len(list_dict.keys()))]:
        print(f"I'm sorry, \"{list}\" is not a valid choice. Please try again.")
        list = input("Which list would you like to make active? ")
    lists.active = list_dict[int(list)]
    print(f"{lists.active.name} is now the active list.")
    _ = input("Press 'return' to continue: ")
    options_page(lists)
    
def undo_page(lists):
    """
    Provides UI to undo last action
    """
    helpers.clear_terminal()
    helpers.print_current_list(lists.active)
    success = lists.active.redo()
    if success:
        print("The last action was undone.")
    else:
        print("Unable to undo the previous action.")
    print("")
    _ = input("Press 'return' to continue: ")
    options_page(lists)
    
def create_list_page(lists):
    """
    create new list
    """
    helpers.clear_terminal()
    name = input("What is the name of the new list you want to create? ")
    answer = input("Would you like to manually create a list (m) or import one (i)? ")
    while answer not in "mi":
        print("invalid response, please enter 'm' or 'i'.")
        answer = input("Would you like to manually create a list (m) or import one (i)? ")
    if answer == "m":
        new_list = ToDoList(name)
        lists.add_list(new_list)
        lists.active = new_list
        print(f"Successfully created new list; {lists.active.name} is now the active list")
    else:
        data = imports.handle_import()
        if data["status"] != "success":
            print("import failed")
        else:
            new_list = ToDoList(name)
            for line in data["data"]:
                if line["name"] == "" or line["value"]=="" or line["estimated_time"]=="":
                    continue
                name = line["name"]
                value = line["value"]
                estimated_time = line["estimated_time"]
                newTask = Task(name, value, estimated_time)
                if line["actual_time"] != "":
                    newTask.update_actual_time(line["actual_time"])
                if line["status"] != "":
                    newTask.update_status(line["actual_time"])
                new_list.add_task(newTask)
                print(f"{newTask} added to list.")
            lists.add_list(new_list)
            lists.active = new_list
    
    _ = input("Press 'return' to continue: ")
    options_page(lists)

def export_list_page(lists):    
    """
    export list to csv using microservice 1
    """
    helpers.clear_terminal()
    pass

def import_list_page(lists):
    """
    import list from csv using microservice 1
    """
    helpers.clear_terminal()
    pass

def switch_list_page(lists):
    """
    Provides UI to switch active list by choosing or creating new active list
    """
    helpers.clear_terminal()
    helpers.print_current_list(lists.active)

    # Show options to user
    options = [
                ("Choose Existing To-Do List.", choose_existing_list_page),
                ("Create New To-Do List.", create_list_page),
                ("Go Back to Options Page.", options_page),
                ("Exit Program.", exit_page)
            ]
    input_text = "Enter the number representing your choice: "
    option = helpers.get_option_num(options, input_text)
    
    # Direct user to requested page
    options[int(option)-1][1](lists)

def exit_page(lists):
    """
    Provides UI to exit program
    """
    helpers.clear_terminal()
    print("Thank you for using the To-Do List App! Goodbye.")
    helpers.pickle_obj(lists)
    helpers.exit_program()

def options_page(lists):
    """
    Provides UI to let users see what they can do with the program
    """
    helpers.clear_terminal()
    helpers.print_current_list(lists.active)

    # Show options to user
    options = [("View To-Do List", view_list_page),
           ("Add task to To-Do List.", add_item_page),
           ("Edit task on To-Do List.", edit_item_page),
           ("Switch Active To-Do List.", switch_list_page),
           ("Export current To-Do List.", export_list_page),
           ("Clear tasks from current To-Do List.", clear_list_page),
           ("Undo last deletion.", undo_page),
           ("Exit Program.", exit_page)
        ]
    input_text = "Enter the number representing your choice: "    
    option = helpers.get_option_num(options, input_text)
    
    # Direct user to requested page
    options[int(option)-1][1](lists)