from to_do_list import Lists, ToDoList, Task
import helpers

client_A = helpers.set_up_client("PORT_A")
client_B = helpers.set_up_client("PORT_B")
client_C = helpers.set_up_client("PORT_C")
client_D = helpers.set_up_client("PORT_D")

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

def change_user_page(lists):
    helpers.clear_terminal()
    
    # Show options to user
    options = [
                ("Create New User", create_user_page),
                ("Login as Existing User", login_page),
                ("Logout", logout_page),
                ("Go Back to Options Page.", options_page),
                ("Exit Program.", exit_page)
            ]
    input_text = "Enter the number representing your choice: "
    option = helpers.get_option_num(options, input_text)
    
    # Direct user to requested page
    options[int(option)-1][1](lists)

def login_page(lists):
    helpers.clear_terminal()
    print(f"You will need to enter your username and password to log in.")
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    client_B.send_pyobj({"action": "login", "username": username, "password": password})
    data = client_B.recv_pyobj()
    if data["status"] != "success":
        print("invalid username or password")
    else:
        lists.active_user = data["current_user"]
        print(f"You have successfully logged in as {lists.active_user}.")
    _ = input("Press 'return' to continue: ")
    options_page(lists)

def create_user_page(lists):
    helpers.clear_terminal()
    print(f"You will need to enter a new username and password to log in.")
    username = input("Please enter your desired username: ")
    password = input("Please enter your desired password: ")
    client_B.send_pyobj({"action": "create", "username": username, "password": password})
    data = client_B.recv_pyobj()
    if data["status"] != "success":
        print("invalid username or password")
    else:
        lists.active_user = data["current_user"]
        print(f"You have successfully logged in as {lists.active_user}.")
    _ = input("Press 'return' to continue: ")
    options_page(lists)  

def logout_page(lists):
    helpers.clear_terminal()
    print(f"You are currently logged in as {lists.active_user}.")
    answer = input(f"Are you sure you want to logout? (y/n)? ")
    while answer not in ["y","n"]:
        print("invalid response, please enter 'y' or 'n'.")
        answer = input("Do you wish to logout (y/n)? ")
    if answer == "n":
        options_page(lists)
    else:
        client_B.send_pyobj({"action": "logout"})
        data = client_B.recv_pyobj()
        if data["status"] != "success":
            print("logout failed")
        else:
            lists.active_user = data["current_user"]
            print(f"You have successfully logged out.")
    _ = input("Press 'return' to continue: ")
    options_page(lists)


def add_item_info_page(lists):
    """
    Provides user with information about adding an item 
    prior to actually adding the item
    """
    helpers.clear_terminal()
    print("To add a task, you will be asked to provide the name of the task, the value of the task (integer between 1 and 10), and the time in hours the task is expected to take.")
    
    # Show options to user
    options = [
                ("Continue to add a task.", add_item_page),
                ("Go Back to Options Page.", options_page),
                ("Exit Program.", exit_page)
            ]
    input_text = "Enter the number representing your choice: "
    option = helpers.get_option_num(options, input_text)
    
    # Direct user to requested page
    options[int(option)-1][1](lists)

def add_item_page(lists):
    """
    Provides UI to add a task to the active list
    """
    helpers.clear_terminal()
    helpers.print_current(lists.active_list, lists.active_user)
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
            lists.active_list.add_task(new_task)
            print(f"Congratulations, you have added {name} to the list.")
            _ = input("Press 'return' to continue: ")
            options_page(lists)
        case "2":
            add_item_info_page(lists)
        case "3":
            options_page(lists)
        case "4":
            exit_page(lists)

def edit_item_page(lists):
    """
    Provides UI to edit a task on the active list
    """
    helpers.clear_terminal()
    helpers.print_current(lists.active_list, lists.active_user)
    lists.active_list.tasks
    for i in range(len(lists.active_list.tasks)):
        print(f"{i+1}. {lists.active_list.tasks[i].name}")
    task = input("Which task would you like to update? ")
    while task not in [str(num + 1) for num in range(len(lists.active_list.tasks))]:
        print(f"I'm sorry, \"{task}\" is not a valid choice. Please try again.")
        task = input("Which task would you like to update? ")
    print(f"You are updating {lists.active_list.tasks[int(task)-1].name}")
    time = input("How many hours did this task take (decimals accepted)? ")
    while not helpers.is_float(time) or float(time) <= 0:
        print("The value must be a positive integer or decimal.")
        time = input("How many hours did this task take (decimals accepted)? ")
    status = ("Enter '1' if they task is not yet started, '2' if the task is in progress, and '3' if the task is completed." )
    while status not in [str(num) for num in range(1,4)]:
        print("The value must be a number between 1 and 3 (inclusive).")
        status = input("Enter '1' if they task is not yet started, '2' if the task is in progress, and '3' if the task is completed." )
    lists.active_list.update_task_time(int(task)-1, time)
    if status == 1:
        status = "Not Started"
    elif status == 2:
        status = "In Progress"
    else:
        status = "Completed"
    lists.active_list.update_task_status(int(task)-1, status)
    print(f"The updated task, {lists.active_list.tasks[int(task)-1].name}, has an updated time of {time} hours and the new status is {status}.")

    _ = input("Press 'return' to continue: ")
    options_page(lists)


def clear_list_page(lists):
    """
    Provides UI to clear the active list of all tasks
    """
    helpers.clear_terminal()
    helpers.print_current(lists.active_list, lists.active_user)

    print(f"Are you sure you want to clear {lists.active_list.name}? This can only be undone until your next deletion action.")
    answer = input("Do you wish to proceed (y/n)? ")
    while answer not in ["y","n"]:
        print("invalid response, please enter 'y' or 'n'.")
        answer = input("Do you wish to proceed (y/n)? ")
    if answer == "y":
        lists.active_list.clear_list()
        print("List has been cleared.\n")
    _ = input("Press 'return' to continue: ")
    options_page(lists)
    

def view_list_page(lists):
    """
    Provides UI to view the active list
    """
    helpers.clear_terminal()
    helpers.print_current(lists.active_list, lists.active_user)
    if lists.active_list.is_empty():
        print("This list is currently empty.")
    else:
        for i in range(len(lists.active_list.tasks)):
            print(f"{i+1}. {lists.active_list.tasks[i]}")
    print("")
    _ = input("Press 'return' to continue: ")
    options_page(lists)

def choose_existing_list_page(lists):
    """
    Provides UI to choose a new active list from existing list of lists
    """
    helpers.clear_terminal()
    helpers.print_current(lists.active_list, lists.active_user)
    list_dict = lists.get_lists_for_user()
    for key, value in list_dict.items():
        print(f"{str(key)}. {value.name}")
    list = input("Which list would you like to make active? ")
    while list not in [str(num + 1) for num in range(len(list_dict.keys()))]:
        print(f"I'm sorry, \"{list}\" is not a valid choice. Please try again.")
        list = input("Which list would you like to make active? ")
    lists.active_list = list_dict[int(list)]
    print(f"{lists.active_list.name} is now the active list.")
    _ = input("Press 'return' to continue: ")
    options_page(lists)
    
def undo_page(lists):
    """
    Provides UI to undo last action
    """
    helpers.clear_terminal()
    helpers.print_current(lists.active_list, lists.active_user)
    success = lists.active_list.redo()
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
        manual_list = ToDoList(name, lists.active_user)
        lists.add_list(manual_list)
        print(f"Successfully created new list; {lists.active_list} is now the active list")
    else:
        client_A.send_pyobj({"action":"import"})
        data = client_A.recv_pyobj()
        if data["status"] != "success":
            print("import failed")
        else:
            new_list = ToDoList(name)
            for line in data["data"]:
                if line["name"] == "" or line["value"]=="" or line["time"]=="":
                    continue
                name = line["name"]
                value = line["value"]
                time = line["time"]
                newTask = Task(name, value, time)
                if line["status"] != "":
                    newTask.update_status(line["status"])
                new_list.add_task(newTask)
                print(f"{newTask} added to list.")
            lists.add_list(new_list)
    
    _ = input("Press 'return' to continue: ")
    options_page(lists)

def export_list_page(lists):    
    """
    export list to csv using microservice 1
    """
    helpers.clear_terminal()
    task_list = [task.task_to_dict() for task in lists.active_list.tasks]
    client_A.send_pyobj({"action":"export", "data": task_list})
    response = client_A.recv_pyobj()
    if response["status"] != "success":
        print("import failed")
    else:
        print(response["message"])

    _ = input("Press 'return' to continue: ")
    options_page(lists)

def statistics_page(lists):
    helpers.clear_terminal()
    tc_lists = lists.get_time_and_completion_lists()
    print(tc_lists[0])
    client_C.send_pyobj({"action": "stats", "lists": tc_lists})
    data = client_C.recv_pyobj()
    if data["status"] != "success":
        print("unable to provide time statistics")
    else:
        print(f"You have successfully spent {data["time"]} hours completing {data["completed"]} tasks. Here are the tasks you've completed:")
        for item in data["task_names"]:
            print(item)
    _ = input("Press 'return' to continue: ")
    options_page(lists)

def switch_list_page(lists):
    """
    Provides UI to switch active list by choosing or creating new active list
    """
    helpers.clear_terminal()
    helpers.print_current(lists.active_list, lists.active_user)

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
    client_B.send_pyobj({"action": "exit"})
    client_C.send_pyobj({"action": "exit"})
    client_D.send_pyobj({"action": "exit"})
    helpers.exit_program()

def options_page(lists):
    """
    Provides UI to let users see what they can do with the program
    """
    helpers.clear_terminal()
    helpers.print_current(lists.active_list, lists.active_user)

    # Show options to user
    options = [("View To-Do List", view_list_page),
           ("Add task to To-Do List.", add_item_info_page),
           ("Edit task on To-Do List.", edit_item_page),
           ("Switch Active To-Do List.", switch_list_page),
           ("Export current To-Do List.", export_list_page),
           ("Clear tasks from current To-Do List.", clear_list_page),
           ("Undo last deletion.", undo_page),
           ("Get Statistics.", statistics_page),
           ("Change User.", change_user_page),
           ("Exit Program.", exit_page)
        ]
    input_text = "Enter the number representing your choice: "    
    option = helpers.get_option_num(options, input_text)
    
    # Direct user to requested page
    options[int(option)-1][1](lists)