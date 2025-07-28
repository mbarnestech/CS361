from collections import defaultdict

class Task:
    not_started = "Not Started"
    in_progress = "In Progress"
    completed = "Completed"

    def __init__(self, name, value, estimated_time, actual_time=None, status=not_started):
        self.name = name
        self.value = value
        self.estimated_time = estimated_time
        self.actual_time = actual_time
        self.status = status

    def __str__(self):
        return f"Task: Name = '{self.name}', Value = {self.value}, Status = {self.status}"
    
    def task_to_dict(self):
        return {"name": self.name,
                "value": self.value,
                "estimated_time": self.estimated_time,
                "actual_time": self.actual_time,
                "status": self.status}
    
    def update_name(self, new_name):
        self.name = new_name
    
    def update_value(self, new_value):
        self.value = new_value

    def update_estimated_time(self, new_estimated_time):
        self.estimated_time = new_estimated_time

    def update_actual_time(self, new_actual_time):
        self.actual_time = new_actual_time
    
    def update_status(self, new_status):
        self.status = new_status

class ToDoList:
    universal = "universal"
    
    def __init__(self, name, owner=universal, tasks=[]):
        self.name = name
        self.owner = owner
        self.tasks = tasks
        self.undo = None

    def __str__(self):
        return f"Current List: Name = '{self.name}', Owner = {self.owner}"
    
    def update_name(self, new_name):
        self.name = new_name
    
    def save_undo(self, num):
        self.undo = (self.tasks[num])

    def delete_task(self, num):
        if not self.valid_num(num):
            return "invalid num"
        self.save_undo(num)
        removed_task = self.tasks.pop(num)
        return removed_task
    
    def update_task_name(self, num, new_name):
        if not self.valid_num(num):
            return "invalid num"
        self.save_undo(num)
        self.tasks[num].name = new_name
    
    def update_task_value(self, num, new_value):
        if not self.valid_num(num):
            return "invalid num"
        self.save_undo(num)
        self.tasks[num].value = new_value

    def update_task_estimated_time(self, num, new_estimated_time):
        if not self.valid_num(num):
            return "invalid num"
        self.save_undo(num)
        self.tasks[num].estimated_time = new_estimated_time

    def update_task_actual_time(self, num, new_actual_time):
        if not self.valid_num(num):
            return "invalid num"
        self.save_undo(num)
        self.tasks[num].actual_time = new_actual_time
    
    def update_task_status(self, num, new_status):
        if not self.valid_num(num):
            return "invalid num"
        self.save_undo(num)
        self.tasks[num].status = new_status

    def valid_num(self, num):
        if num < len(self.tasks):
            return True
        return False

class Lists:

    def __init__(self, name = "List of Lists"):
        self.name = name
        self.lists = {}

    def add_list(self, list):
        self.lists.setdefault(list.owner, []).append(list)
    
    def is_empty(self):
        return len(self.lists.keys()) == 0