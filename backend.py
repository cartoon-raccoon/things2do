import json
from datetime import datetime, date, time
from configparser import ConfigParser

todofile = 'todolist.json'

def add_todo(taskname, deadline, priority, reminder, deleteflag):
    task = {
        'name':taskname,
        'deadline':deadline,
        'priority': priority,
        'autodel':deleteflag
    }
    with open(todofile, 'a') as todo:
        jdump = json.dumps(task) + '\n'
        todo.write(jdump)

def read_todo():
    with open(todofile, 'r') as todo:
        for task in todo:
            task = json.loads(task)
            print(f"Task: {task['name']}")
            print(f"Deadline: {task['deadline']}")

def remove_todo(taskname):
    """
    reads the entire file line by line into a list and deletes the entry
    rewrites the entire file
    """
    tasks = []
    with open(todofile, 'r') as todo:
        tasks = todo.readlines()
        for i, task in enumerate(tasks):
            task = json.loads(task)
            if task['name'] == taskname:
                del tasks[i]
                break
    with open(todofile, 'w') as todo:
        for task in tasks:
            todo.write(task)

if __name__ =='__main__':
    # add_todo('sleep', 'today', 'low', 5, True)
    # add_todo('commit suicide', 'today', 'high', 2, False)
    # read_todo()
    # remove_todo('sleep')
    # read_todo()
    now = datetime.now()
    day = date(2020, '1g', 27)
    today = date.today()
    print(now.strftime('%H:%M:%S'))
    print(str(today))
    print(day)