from collections import defaultdict

universal = "Public"

class Task:
    """
    A Task on a To-Do List
    """
    not_started = "Not Started"
    in_progress = "In Progress"
    completed = "Completed"

    def __init__(self, name, value, time, status=not_started):
        """
        initializes class
        """
        self.name = name
        self.value = value
        self.time = time
        self.status = status

    def __str__(self):
        """
        sets string representation of the class
        """
        return f"Name = '{self.name}', {self.value=}, {self.time=}, Status = {self.status}"
    
    def task_to_dict(self):
        """
        returns a dictionary object of the task
        """
        return {"name": self.name,
                "value": self.value,
                "time": self.time,
                "status": self.status}
    
    def update_time(self, new_time):
        """
        update task time
        """
        self.time = new_time

    def update_status(self, new_status):
        """
        update task status
        """
        self.status = new_status

class ToDoList:
    """
    A Single To-Do List
    """
    def __init__(self, name, owner=universal, tasks=[]):
        """
        initializes class
        """
        self.name = name
        self.owner = owner
        self.tasks = tasks
        self.undo = None

    def __str__(self):
        """
        sets string representation of the class
        """
        return f"Current List: Name = '{self.name}', Owner = {self.owner}"
    
    def update_name(self, new_name):
        """
        updates the list name
        """
        self.name = new_name
    
    def save_undo(self, type, info):
        """
        saves the last type of action done and the information necessary to undo that action
        """
        self.undo = (type, info)

    def delete_task(self, num):
        """
        allows user to delete a specific task with the ability to undo later
        """
        if not self.valid_num(num):
            return "invalid num"
        self.save_undo("delete task", self.tasks[num])
        removed_task = self.tasks.pop(num)
        return removed_task
    
    def update_task_time(self, num, new_time):
        """
        allows user to update time with the ability to undo later
        """
        if not self.valid_num(num):
            return "invalid num"
        self.tasks[num].time = new_time

    def update_task_status(self, num, new_status):
        """
        allows user to update status with the ability to undo later
        """
        if not self.valid_num(num):
            return "invalid num"
        self.tasks[num].status = new_status

    def valid_num(self, num):
        """
        returns whether an index is valid for getting an item from the list
        """
        if num < len(self.tasks):
            return True
        return False
    
    def is_empty(self):
        """
        returns bool of whether list is empty
        """
        return len(self.tasks) == 0
    
    def add_task(self, task):
        """
        adds a task to the list
        """
        self.tasks.append(task)
    
    def clear_list(self):
        """
        clears all tasks from the list
        """
        self.save_undo("clear list", self.tasks)
        self.tasks = []
    
    def redo(self):
        """
        allows for a single action to be undone
        """
        if not self.undo:
            return False
        match self.undo[0]:
            case "clear list":
                print("If you have added items since clearing the list, your new items will be cleared.")
                answer = input("Do you wish to proceed (y/n)? ")
                while answer not in "yn":
                    print("invalid response, please enter 'y' or 'n'.")
                    answer = input("Do you wish to proceed (y/n)? ")
                if answer == "y":
                    self.tasks = self.undo[1]
                else:
                    return False
            case "delete task":
                self.tasks.append(self.undo[1])
            case _:
                return False
        self.undo = None
        return True


class Lists:
    """
    A class to organize all To Do Lists in the app
    """

    def __init__(self, name = "List of Lists", active = ToDoList("My First List")):
        """
        initializes class
        """
        self.name = name
        self.lists = defaultdict(list)
        self.lists[active.owner].append(active)
        self.active_list = active
        self.active_user = active.owner

    def add_list(self, list):
        """
        add a to-do list to the lists
        """
        self.lists[list.owner].append(list)
        self.active_list = list
    
    def is_empty(self):
        """
        return bool of whether there are any lists
        """
        return len(self.lists.keys()) == 0
    
    def get_lists_for_user(self, user=universal):
        """
        make a dictionary of all accessible lists for a given user
        """
        list_dict = {}
        count = 1
        if user != universal:
            for list in self.lists[user]:
                list_dict[count] = list
                count+=1
        for list in self.lists[universal]:
            list_dict[count] = list
            count+=1
        
        return list_dict

    def get_time_and_completion_lists(self):
        print('getting time and completion list')
        tc_list = []
        if self.active_user != universal:
            for list in self.lists[self.active_user]:
                for task in list.tasks:
                    tc_list.apppend([task.name, task.time, task.status])
                    print(tc_list)
        for list in self.lists[universal]:
                for task in list.tasks:
                    tc_list.append([task.name, task.time, task.status])
                    print(tc_list)
        return tc_list
