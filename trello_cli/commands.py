from dotenv import load_dotenv, find_dotenv
from trello import TrelloClient
from datetime import date, timedelta
from datetime import datetime

import os, json
from docopt import docopt
load_dotenv(find_dotenv())

client = TrelloClient(
  api_key=os.environ.get("TRELLO_API_KEY"),
  api_secret=os.environ.get("TRELLO_API_SECRET")
)

def get_last_tuesday():
    today = date.today()
    offset = (today.weekday() - 2) % 7
    last_tuesday = today - timedelta(days=offset)
    return last_tuesday

def get_first_day_of_month():
    return date.today().replace(day=1)

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

def moved_to(daterange, output_type, after_list_name):
    boards = client.list_boards()

    since_date = get_last_tuesday()
    if daterange == 'day':
        since_date = datetime.today()
    elif daterange == 'month':
        since_date = get_first_day_of_month()


    board_actions = {}
    for board in boards:
        actions = board.fetch_actions("updateCard:idList", since=since_date, before=datetime.now(), action_limit=1000)
        
        moved_to_done = []
        for action in actions:
            if action["data"]["listAfter"]["name"].lower() == after_list_name:
                new_object = {}
                if output_type == 'json':
                    new_object["date"] = action["date"]
                else:
                    new_object["date"] = datetime.strptime(action["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                new_object["card"] = action["data"]["card"]
                new_object["board"] = action["data"]["board"]
                new_object["prevList"] = action["data"]["listBefore"]

                moved_to_done.append(new_object)

        if len(moved_to_done) > 0:
            board_name = moved_to_done[0]["board"]["name"]
            if output_type is 'console':
                print("\n\nFor Board: " + board_name + "\n============================\n")

                for obj in moved_to_done:
                    date_str = "{:%b %d, %Y}".format(new_object["date"])
                    print("Card: '" + obj["card"]["name"] + "' moved to 'Done' from '" + obj["prevList"]["name"] + "' on " + date_str)
        
            board_actions[board_name] = moved_to_done

    if output_type == 'json':
        board_actions = json.dumps(board_actions)
        print(board_actions)

    return board_actions

def moved_to_done(daterange, output_type):
    return moved_to('done')

def moved_to_sprint(daterange, output_type):
    return moved_to('sprint')

def moved_to_backlog(daterange, output_type):
    return moved_to('backlog')



valid_dateranges = ['today', 'week', 'month']

class Completed(AbstractCommand):
    """
    Retrieves completed tickets for a user
    usage:
        completed [--date=<daterange>]
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
        --type=<valid_ticket_types>     View assigned tickets with type <type>
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


valid_time_ranges = ["day", "week", "month"]
valid_ouput_formats = ["console", "json"]

class Report(AbstractCommand):
    """
    Generates Daily/Weekly/Monthly Report for User (defaults to weekly)

    usage:
        report <to_list_name> [--range=<valid_time_ranges>] [--output=<valid_ouput_formats>]

    options:
        --range=<valid_time_ranges>     Generate report for user during <valid_time_range> (default is 'weekly')
        --output=<valid_ouput_formats>   Generate report with specified output (default is 'console')
    """

    def execute(self):
        if '--range' not in self.args or self.args['--range'] is None:
            self.args['--range'] = 'week'
        if '--output' not in self.args or self.args['--output'] is None:
            self.args['--output'] = 'console'

        to_list_name = self.args.pop('<to_list_name>')
        if self.args['--range'] in valid_time_ranges and self.args['--output'] in valid_ouput_formats:
            print("Trello Ticket Report:\n--------------------\n")
            actions = moved_to(self.args['--range'], self.args['--output'], to_list_name)
        elif self.args['--range'] not in valid_time_ranges:
            print('{} is not a valid time range type. Valid ticket type are "day", "week" and "month"'.format(self.args['--range']))
            return
        else:
            print('{} is not a valid ouput format. Valid output formats are "console" and "json"'.format(self.args['--output']))


