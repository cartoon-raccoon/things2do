import json
from datetime import datetime, date, time
from configparser import ConfigParser

todofile = 'todolist.json'

def add_todo(taskname, deadline, priority, reminder, deleteflag):
    task = {
        'name':taskname,
        'deadline':str(deadline),
        'priority': priority,
        'no_del':deleteflag
    }

    if not exists(task['name']):
        with open(todofile, 'a') as todo:
            jdump = json.dumps(task) + '\n'
            todo.write(jdump)
            return 0
    else:
        return 1

def read_todo(taskname):
    with open(todofile, 'r') as todo:
        for task in todo:
            task = json.loads(task)
            if task['name'] == taskname:
                return [task['name'], 
                        task['deadline'], 
                        task['priority']]
        return None

def remove_todo(taskname):
    """
    reads the entire file line by line into a list and deletes the entry
    rewrites the entire file
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

def exists(taskname):
    with open(todofile, 'r') as todo:
        tasks = todo.readlines()
        for task in tasks:
            try:
                task = json.loads(task)
                if task['name'] == taskname:
                    return True
            except json.decoder.JSONDecodeError:
                return False
        return False

if __name__ =='__main__':
    add_todo('sleep', 'today', 'low', 5, True)
    add_todo('commit suicide', 'today', 'high', 2, False)
    read_todo('sleep')
    #remove_todo('sleep')
    read_todo('commit suicide')
    now = datetime.now()
    day = date(2020, 10, 27)
    today = date.today()
    print(now.strftime('%H:%M:%S'))
    print(str(today))
    print(day)