import sys
from datetime import datetime
import click
from tabulate import tabulate
import backend

@click.group(invoke_without_command=True)
@click.pass_context
#@click.option('-a', '--all', is_flag=True, help='List all active tasks.')
def cli(ctx):
    if ctx.invoked_subcommand is None:
        deleted, success = backend.autodel()
        if not success:
            click.echo("ERROR: autodelete failed.")
            sys.exit(1)
        tasks = backend.printall()

        if tasks is None:
            click.echo("No active tasks to display.")
            sys.exit(0)
        elif tasks == 1:
            click.echo("An error occurred while reading tasks from the file.")
            sys.exit(1)
        
        if deleted == 1:
            click.echo("1 task was auto-deleted.\n")
        elif deleted > 1:
            click.echo(f"{deleted} tasks were auto-deleted.")

        click.echo("Displaying all active tasks:\n")
        print(tabulate(tasks, headers="keys"))

@cli.command() #add command
@click.argument('task')
@click.option('-d', '--deadline', default=None, type=str,
    help='''The deadline for the task. Use DD-MM-YYYY@HH:MM and zero-padded 24 hour time. 
            If the deadline is today, you can replace the date with "today".''')
@click.option('-p', '--priority', default='low', 
    help='Urgency of the task, defaults to low. Accepted values: Low, Medium, High.')
@click.option('-r', '--remindme', default=None, 
    help='Specify a reminder in hours before the deadline.')
@click.option('--nodelete', default=False, is_flag=True, 
    help='Set this flag to prevent t2d from auto-deleting this task.')
def add(task, deadline, priority, remindme, nodelete):
    if backend.exists(task):
        click.echo(f"Task '{task}' already exists.")
        sys.exit(0)
    #setting internal vars from fxn args
    no_delete = nodelete
    reminder = remindme

    #if one of the options was left blank, causing click to interpret --nodelete as option's arg
    for arg in [deadline, priority, remindme]:
        if arg == '--nodelete':
            no_delete = True

    dline = None
    if deadline is not None:
        if deadline[0:5] == 'today':
            deadline = deadline.replace('today', 
                datetime.today().strftime('%d-%m-%Y'))
        try:
            dline = datetime.strptime(deadline, "%d-%m-%Y@%H:%M")
        except:
            click.echo("Invalid deadline set.")
            sys.exit(1)
        if dline < datetime.today():
            click.echo("Specified deadline is already past.")
            sys.exit(0)

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
        reminder = None
        click.echo("No reminder set.")
    elif not dline and reminder:
        click.echo("No deadline set, cannot set reminder.")
    else:
        click.echo(f"Reminder set for {reminder} hour(s) before deadline")
    
    click.echo(f"Priority set to {priority}")
    
    #logic control for deadline and auto-delete relationship
    if not dline and not no_delete:
        click.echo("Warning: This task cannot be auto-deleted as there is no deadline set.")
        no_delete = True
    elif not dline and no_delete:
        click.echo("This task cannot be auto-deleted as there is no deadline set.")
    elif no_delete and dline:
        click.echo("This task will not be automatically deleted.")
    else:
        click.echo("This task will be automatically deleted when deadline passes.")

    result = backend.add_todo(task, dline, priority, reminder, no_delete)
    if result == 0:
        click.echo("\nTask successfully added!")
    elif result == 1:
        click.echo(f"\nAn error occurred. Please check if the task was added or try again.")
        sys.exit(1)
    
@cli.command()
@click.argument('task')
def remove(task):
    if backend.remove_todo(task):
        click.echo(f"Successfully removed task: {task}")
    else:
        click.echo("Error: task does not exist.")
        sys.exit(1)

@cli.command()
@click.argument('task')
@click.option('-d', '--deadline', default=None, type=str,
                help="""Edits the deadline for the specified task. 
                Type 'remove' to remove the deadline.""")
@click.option('-p', '--priority', default=None,
                help="Edits the priority for the task.")
@click.option('-r', '--remindme', default=None,
                help="Edits the reminder if not already set.")
#TODO: Refactor this pile of crap into something that doesn't repeat itself
#Factor out the logic checking and implement a separate function that does that
def edit(task, deadline, priority, remindme):
    check_task = backend.read_todo(task)
    if check_task is None:
        click.echo("Task not found.")
        sys.exit(1)
    no_delete = check_task[4] #index 4 is the no delete flag returned by read_todo()
    click.echo(f'Edited task: {check_task[0]}')
    if deadline =='remove' and check_task[4] == False:
        click.echo("This task will no longer be auto-deleted.")
        no_delete = True
    #TODO: Factor this out into a separate function to be called by this and add()
    dline = None
    if deadline != 'remove' and deadline is not None:
        if deadline[0:5] == 'today':
            deadline = deadline.replace('today', 
                datetime.today().strftime('%d-%m-%Y'))
        try:
            dline = datetime.strptime(deadline, "%d-%m-%Y@%H:%M")
        except:
            click.echo("Invalid deadline set.")
            sys.exit(1)
        if dline < datetime.today():
            click.echo("Specified deadline is already past.")
            sys.exit(0)
    elif deadline == "remove":
        dline = "None"
    #------------------------------------------------#
    result = backend.edit_todo(task, dline, remindme, priority, no_delete)
    if result is not None:
        if result:
            click.echo("Task successfully edited.")
        else:
            click.echo("Error: Task does not exist.")
    else:
        click.echo("There was an error editing the task. Check that the task has been edited properly.")
        sys.exit(1)
    

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