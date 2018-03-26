#! /usr/bin/env python
"""
CLI interface for Trello

usage:
    trello <command> [<args>...]

options:
    -h, --help                  shows the help
    -v, --version               shows the version

The subcommands are:
    assigned              View tickets assigned to you
    completed             View tickets completed by you (date range defaults to today)
"""

from docopt import docopt
from docopt import DocoptExit

import commands

def main():
    args = docopt(__doc__, version='0.0.3', options_first=True)

    # Retrieve the command to execute.
    command_name = args.pop('<command>').capitalize()

    # Retrieve the command arguments.
    command_args = args.pop('<args>')
    if command_args is None:
        command_args = {}

    # After 'poping' '<command>' and '<args>', what is left in the args dictionary are the global arguments.

    # Retrieve the class from the 'commands' module.
    try:
        command_class = getattr(commands, command_name)
    except AttributeError:
        print('Unknown command. RTFM!.')
        raise DocoptExit()

    # Create an instance of the command.
    command = command_class(command_args, args)

    # Execute the command.
    command.execute()

main()