import click
import sys

@click.group(invoke_without_command=True)
@click.option('-a', '--all', is_flag=True, help='List all active tasks.')
def cli(all):
    if all:
        click.echo("Displaying all active tasks.")

@cli.command() #add command
@click.argument('task')
@click.option('-d', '--deadline', default=None, help='The deadline for the task.')
@click.option('-r', '--remindme', default=None, 
    help='Specify a reminder in hours before the deadline.')
@click.option('--nodelete', default=False, is_flag=True, 
    help='Set this flag to prevent t2d from auto-deleting this task.')
def add(task, deadline, remindme, nodelete):
    no_delete = nodelete

    #handling invalid reminder input because click doesn't check for it
    try:
        reminder=int(remindme)
    except:
        #if -r was left blank, causing click to interpret --nodelete as -r's input
        if remindme == '--nodelete':
            no_delete = True
        reminder=None
        click.echo("Invalid reminder set, defaulting to no reminder.")
    
    click.echo(f"\nSUMMARY:\nSet task: {task}")

    #logic control for deadline and reminder interrelations
    click.echo(f"Deadline: {deadline}")
    if not reminder:
        click.echo("No reminder set.")
    elif not deadline and reminder:
        click.echo("No deadline set, cannot set reminder.")
    else:
        click.echo(f"Reminder set for {reminder} hour(s) before deadline")
    
    #logic control for deadline and auto-delete relationship
    if not deadline and not no_delete:
        click.echo("Warning: This task cannot be auto-deleted as there is no deadline set.")
    elif not deadline and no_delete:
        click.echo("This task cannot be auto-deleted as there is no deadline set.")
    elif no_delete and deadline:
        click.echo("This task will not be automatically deleted.")
    else:
        click.echo("This task will be automatically deleted when deadline passes.")

@cli.command()
@click.argument('task')
def remove(task):
    click.echo(f"Removing task: {task}")

@cli.command()
@click.argument('task')
#what options needed for edit?
def edit(task):
    click.echo(f'Editing task: {task}')

@cli.command()
@click.argument('task')
@click.option('-r', '--regex', is_flag=True, default=False)
def search(task, regex):
    if regex:
        click.echo(f"Searching for tasks matching regex {task}")
    else:
        click.echo(f"Searching for task: {task}")