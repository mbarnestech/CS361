universal = "Public"

class Task:
    """
    A Task on a To-Do List
    """
    not_started = "Not Started"
    in_progress = "In Progress"
    completed = "Completed"

    def __init__(self, name, value, estimated_time, actual_time=None, status=not_started):
        """
        initializes class
        """
        self.name = name
        self.value = value
        self.estimated_time = estimated_time
        self.actual_time = actual_time
        self.status = status

    def __str__(self):
        """
        sets string representation of the class
        """
        return f"Name = '{self.name}', Status = {self.status}"
    
    def task_to_dict(self):
        """
        returns a dictionary object of the task
        """
        return {"name": self.name,
                "value": self.value,
                "estimated_time": self.estimated_time,
                "actual_time": self.actual_time,
                "status": self.status}
    
    def update_name(self, new_name):
        """
        update task name
        """
        self.name = new_name
    
    def update_value(self, new_value):
        """
        update task value
        """
        self.value = new_value

    def update_estimated_time(self, new_estimated_time):
        """
        update task estimated time
        """
        self.estimated_time = new_estimated_time

    def update_actual_time(self, new_actual_time):
        """
        update task actual time
        """
        self.actual_time = new_actual_time
    
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
    
    def update_task_name(self, num, new_name):
        """
        allows user to update task name with the ability to undo later
        """
        if not self.valid_num(num):
            return "invalid num"
        self.save_undo(num)
        self.tasks[num].name = new_name
    
    def update_task_value(self, num, new_value):
        """
        allows user to update task value with the ability to undo later
        """
        if not self.valid_num(num):
            return "invalid num"
        self.save_undo(num)
        self.tasks[num].value = new_value

    def update_task_estimated_time(self, num, new_estimated_time):
        """
        allows user to update estimated time with the ability to undo later
        """
        if not self.valid_num(num):
            return "invalid num"
        self.save_undo(num)
        self.tasks[num].estimated_time = new_estimated_time

    def update_task_actual_time(self, num, new_actual_time):
        """
        allows user to update actual time with the ability to undo later
        """
        if not self.valid_num(num):
            return "invalid num"
        self.save_undo(num)
        self.tasks[num].actual_time = new_actual_time
    
    def update_task_status(self, num, new_status):
        """
        allows user to update status with the ability to undo later
        """
        if not self.valid_num(num):
            return "invalid num"
        self.save_undo(num)
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
        self.lists = {active.owner: [active]}
        self.active = active

    def add_list(self, list):
        """
        add a to-do list to the lists
        """
        self.lists.setdefault(list.owner, []).append(list)
    
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


