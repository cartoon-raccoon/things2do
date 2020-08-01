import os
import json
from datetime import datetime, date, time
from configparser import ConfigParser

todofile = ''

config = ConfigParser()
if 'config.ini' not in os.listdir("."):
    pass
else:
    pass
    
config.read('/home/raccoon/Projects/Things2Do/config.ini')
todofile = config['General']['filepath']

def add_todo(taskname, deadline, priority, reminder, deleteflag):
    """ 
    Writes a single task to the todolist.json file.
    Accepted params are the options specified in the frontend
    """
    autodel()
    task = {
        'name': taskname,
        'deadline': str(deadline),
        'priority': priority,
        'reminder': reminder,
        'no_del': deleteflag
    }

    if not exists(task['name']):
        with open(todofile, 'a') as todo:
            try:
                jdump = json.dumps(task) + '\n'
                todo.write(jdump)
                return 0
            except:
                return 1

def read_todo(taskname):
    """
    Looks for a task with a specified name and returns a list with its attributes
    """
    autodel()
    with open(todofile, 'r') as todo:
        for task in todo:
            task = json.loads(task)
            if taskname in task['name']:
                return [task['name'], 
                        task['deadline'], 
                        task['priority']]
        return None

def remove_todo(taskname):
    """
    Reads the entire file line by line into a list and deletes the entry,
    then rewrites the entire file
    """
    tasks = []
    found = False #track if todo item was found
    with open(todofile, 'r') as todo:
        tasks = todo.readlines()
        for i, task in enumerate(tasks):
            task = json.loads(task)
            if task['name'] == taskname:
                del tasks[i]
                found = True
                break

    with open(todofile, 'w') as todo:
        for task in tasks:
            todo.write(task)
    
    return found

def edit_todo(taskname, deadline, reminder, priority, deleteflag):
    """
    Edits the task specified by taskname
    """
    edit_task = ''
    editables = ['deadline', 'reminder', 'priority', 'no_del']
    edited = [deadline, reminder, priority, deleteflag]

    if not exists(taskname):
        return False

    with open(todofile, 'r') as todo:
        tasks = todo.readlines()
        for task in tasks:
            try:
                task = json.loads(task)
                if taskname == task['name']:
                    edit_task = task
                    break
            except json.decoder.JSONDecodeError:
                return None
    
    remove_todo(taskname)

    for i, editable in enumerate(editables):
        if edited[i] is not None:
            edit_task[editable] = edited[i]

    with open(todofile, 'a') as todo:
        try:
            todo.write(json.dumps(edit_task))
        except json.decoder.JSONDecodeError:
            return None
    return True


def exists(taskname):
    """
    Checks whether a tasks of that name exists in the todofile
    """
    with open(todofile, 'r') as todo:
        tasks = todo.readlines()
        for task in tasks:
            try:
                task = json.loads(task)
                if taskname == task['name']:
                    return True
            except json.decoder.JSONDecodeError:
                return False
        return False

def autodel(): #i hate this code so much
    """
    Runs whenever the app is run, deletes any expired tasks
    """
    today, tasks = datetime.today(), []
    to_remove_indexes = []
    deleted_tasks = 0

    with open(todofile, 'r') as todo:
        tasks = todo.readlines()
        for i, task in enumerate(tasks):
            try:
                task = json.loads(task)
            except json.decoder.JSONDecodeError:
                return False, False
            dline = datetime.strptime(task['deadline'], "%Y-%m-%d %H:%M:%S")
            if dline < today and not task['no_del']:
                to_remove_indexes.append(i)
                deleted_tasks += 1

    for index in to_remove_indexes[::-1]:
        del tasks[index]
    
    with open(todofile, 'w') as todo:
        for task in tasks:
            todo.write(task)
    
    return deleted_tasks, True

def printall():
    """
    Returns a dictionary of all the tasks present in the todofile, sorted by deadline
    """
    all_tasks = {
        'Name': [],
        'Deadline':[],
        'Priority':[],
        'Autodelete':[]
    }
    with open(todofile, 'r') as todo:
        try: #list compre for loading dict objs in to list, sorting by deadline
            tasks = sorted([json.loads(task) for task in todo.readlines()], 
                    key= lambda task: task['deadline'])
        except json.decoder.JSONDecodeError:
            return 1
        if not tasks:
            return None
        for task in tasks:
            all_tasks['Name'].append(task['name'])
            all_tasks['Deadline'].append(task['deadline'])
            all_tasks['Priority'].append(task['priority'])
            all_tasks['Autodelete'].append(
                'No' if task['no_del'] else 'Yes')
    return all_tasks

def config_exists(): #this is a stupid function idk why i wrote this
    return False if 'config.ini' not in os.listdir(".") else True

def setup():
    pass

if __name__ == '__main__':
    # add_todo('sleep', 'today', 'low', 5, True)
    # add_todo('commit suicide', 'today', 'high', 2, False)
    # read_todo('sleep')
    # #remove_todo('sleep')
    # read_todo('commit suicide')
    # now = datetime.now()
    # day = date(2020, 10, 27)
    #today = date.today()
    print(config_exists())
    print(config['General']['filepath'])