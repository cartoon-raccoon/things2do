import click
import sys
import backend
from datetime import datetime

@click.group(invoke_without_command=True)
@click.option('-a', '--all', is_flag=True, help='List all active tasks.')
def cli(all):
    if all:
        click.echo("Displaying all active tasks.")

@cli.command() #add command
@click.argument('task')
@click.option('-d', '--deadline', default=None, type=str,
    help='The deadline for the task. Use DD-MM-YYYY@HH-MM and 24 hour time.')
@click.option('-p', '--priority', default='low', 
    help='Urgency of the task, defaults to low. Accepted values: Low, Medium, High.')
@click.option('-r', '--remindme', default=None, 
    help='Specify a reminder in hours before the deadline.')
@click.option('--nodelete', default=False, is_flag=True, 
    help='Set this flag to prevent t2d from auto-deleting this task.')
def add(task, deadline, priority, remindme, nodelete):
    #setting internal vars from fxn args
    no_delete = nodelete
    reminder = remindme

    #if one of the options was left blank, causing click to interpret --nodelete as option's arg
    for arg in [deadline, priority, remindme]:
        if arg == '--nodelete':
            no_delete = True

    dline = None
    if deadline is not None:
        deaddate, deadtime = deadline[:10].split('-'), deadline[11:].split('-')
        try:
            dline = datetime(int(deaddate[2]), 
                             int(deaddate[1]), 
                             int(deaddate[0]), 
                             hour=int(deadtime[0]),
                             minute=int(deadtime[1]))
        except Exception as err:
            click.echo("Invalid deadline set.")
            sys.exit(1)

    if priority.lower() not in ['low', 'medium', 'mid', 'high']:
        click.echo("Invalid priority set.")
        sys.exit(1)

    #handling invalid reminder input because click doesn't check for it
    if reminder is not None:
        try:
            reminder=int(reminder)
        except:
            click.echo("Invalid reminder set.")
            sys.exit(1)
        if reminder < 0:
            click.echo("Invalid reminder set.")
            sys.exit(1)
    
    click.echo(f"\nSUMMARY:\nSet task: {task}")
    if dline is not None:
        click.echo(f"Deadline: {dline.date()} at {dline.time()}")
    else:
        click.echo("No deadline set.")

    #logic control for deadline and reminder interrelations
    if not reminder:
        click.echo("No reminder set.")
    elif not deadline and reminder:
        reminder = None
        click.echo("No deadline set, cannot set reminder.")
    else:
        click.echo(f"Reminder set for {reminder} hour(s) before deadline")
    
    click.echo(f"Priority set to {priority}")
    
    #logic control for deadline and auto-delete relationship
    if not deadline and not no_delete:
        click.echo("Warning: This task cannot be auto-deleted as there is no deadline set.")
    elif not deadline and no_delete:
        click.echo("This task cannot be auto-deleted as there is no deadline set.")
    elif no_delete and deadline:
        click.echo("This task will not be automatically deleted.")
    else:
        click.echo("This task will be automatically deleted when deadline passes.")
    
    result = backend.add_todo(task, dline, priority, reminder, no_delete)
    if result == 0:
        click.echo("\nTask successfully added!")
    elif result == 1:
        click.echo(f"\nTask '{task}' already exists.")

@cli.command()
@click.argument('task')
def remove(task):
    if backend.remove_todo(task):
        click.echo(f"Successfully removed task {task}")
    else:
        click.echo(f"Error: task does not exist.")
        sys.exit(1)

@cli.command()
@click.argument('task')
#what options needed for edit?
def edit(task):
    click.echo(f'Editing task: {task}')

@cli.command()
@click.argument('task')
@click.option('-r', '--regex', is_flag=True, default=False,
    help='Treat the argument as a regular expression.')
def search(task, regex):
    if regex:
        click.echo(f"Searching for tasks matching regex {task}")
    else:
        result = backend.read_todo(task)
        if result is not None:
            click.echo(f"Task: {result[0]} \nDeadline: {result[1]} \nPriority: {result[2]}")
        else:
            click.echo("Task not found.")