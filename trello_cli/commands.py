from dotenv import load_dotenv, find_dotenv
from trello import TrelloClient

import os
from docopt import docopt
load_dotenv(find_dotenv())

client = TrelloClient(
  api_key=os.environ.get("API_KEY"),
  api_secret=os.environ.get("API_SECRET")
)

class AbstractCommand:
    """Base class for the commands"""

    def __init__(self, command_args, global_args):
        """
        Initialize the commands.

        :param command_args: arguments of the command
        :param global_args: arguments of the program
        """
        self.args = docopt(self.__doc__, argv=command_args)
        self.global_args = global_args

    def execute(self):
        """Execute the commands"""
        raise NotImplementedError

def completed():
    return client.search("@me list:done is:open", False, ["cards"])

def completed_daterange(edited_daterange):
    return client.search("@me list:done edited:" + edited_date_range + " is:open", False, ["cards"])

def assigned():
    return client.search("@me is:open", False, ["cards"])

def assigned_type(list_type):
    return client.search("@me list:" + list_type + " is:open", False, ["cards"])

valid_dateranges = ['today', 'week', 'month']

class Completed(AbstractCommand):
    """
    Retrieves completed tickets for a user
    usage:
        completed ( --date=<daterange>)
    options:
        --date=<daterange>
    """

    def execute(self):
        if not self.args['--date']:
            print("Completed Tickets Are:\n--------------------\n")
            tickets = completed()
            for ticket in tickets:
                print(ticket)
                print("\n")
        elif self.args['--date'] in valid_dateranges:
            print("Completed Tickets Are:\n--------------------\n")
            tickets = completed_daterange(args['--date'])
            for ticket in tickets:
                print(ticket)
                print("\n")
        else:
            print('{} is not a valid daterange. Valid date ranges are "today", "week" or "month"'.format(self.global_args['--date']))
            return

valid_ticket_types = ["sprint", "done"]

class Assigned(AbstractCommand):
    """
    Gets assigned tickets for user

    usage:
        assigned

    options:
        --type=<meters>     Player jumps for <meters> meters.
    """

    def execute(self):
        if '--type' not in self.args:
            print("Completed Tickets Are:\n--------------------\n")
            tickets = assigned()
            for ticket in tickets:
                print(ticket)
                print("\n")

        elif self.args['--type'] in valid_ticket_types:
            print("Completed Tickets Are:\n--------------------\n")
            tickets = assigned_type(args['--type'])
            for ticket in tickets:
                print(ticket)
                print("\n")
        else:
            print('{} is not a valid ticket type. Valid ticket type are "sprint" and "done"'.format(self.global_args['--type']))
            return

