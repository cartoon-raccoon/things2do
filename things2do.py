import click
import sys

@click.group(invoke_without_command=True)
@click.option('-a', '--all', is_flag=True)
def cli(all):
    if all:
        click.echo("Displaying all active tasks.")

@cli.command()
@click.argument('task')
@click.option('-d', '--deadline', default=None)
@click.option('-r', '--remindme', default=False, is_flag=True)
@click.option('--nodelete', default=False, is_flag=True)
def add(task, deadline, remindme, nodelete):
    click.echo(f"Set task: {task}")

    #logic control for deadline and reminder interrelations
    click.echo(f"Deadline: {deadline}")
    if not remindme:
        click.echo("No reminder set.")
    elif not deadline and remindme:
        click.echo("No deadline set, cannot set reminder.")
    else:
        click.echo(f"Reminder set for {deadline}")
    
    #logic control for deadline and auto-delete relationship
    if not deadline and not nodelete:
        click.echo("Warning: This task cannot be auto-deleted as there is no deadline set.")
    elif not deadline and nodelete:
        click.echo("This task cannot be auto-deleted as there is no deadline set.")
    elif nodelete and deadline:
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