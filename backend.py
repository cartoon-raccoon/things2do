import json
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

if __name__ =='__main__':
    add_todo('sleep', 'today', 'low', 5, True)
    add_todo('commit suicide', 'today', 'high', 2, False)
    read_todo()