#!/usr/bin/env python
from jira.client import JIRA
from jira.client import GreenHopper
from jira import JIRAError
import argparse
import getpass
import sys


def parse_arguments():
    parser = argparse.ArgumentParser(description='Gather some statistics about a JIRA sprint')
    parser.add_argument('--user', metavar='USER',  help='The JIRA user name to used for auth. If omitted the current user name will be used.')
    parser.add_argument('--password', metavar='PASSWORD',  help='The JIRA password to be used for auth. If omitted you will be prompted.')
    parser.add_argument('--list-boards', action='store_true', help='When supplied, a list of RapidBoards and their associated IDs are displayed')
    parser.add_argument('--server',  default='https://pagerduty.atlassian.net')
    parser.add_argument('board', nargs="?", help='The id of the rapidboard that houses the sprint on which you want to gather stats. (Use --list-boards to find it')
    parser.add_argument('sprint', nargs="?", help='The name of the sprint on which to produce the stats')

    args = parser.parse_args()
    return args

def find_custom_field(field_name, jira):
    fields = jira.fields()
    for f in fields:
        if field_name in f['clauseNames']:
            return f

def gather_stats(issues, jira):
    stats = {}
    velocity = 0
    story_point_field = find_custom_field("Story Points", jira)
    if not story_point_field:
        raise Exception("Couldn't find the story points custom field for this jira instance")

    for issue in issues:
        if issue.typeName != "SubTask":
            iss = jira.issue(issue.key)
            velocity += getattr(iss.fields, story_point_field['id'])
    stats['velocity'] = velocity
    return stats

def print_issues(title, issues):
    print title
    print "=" * len(title)
    for issue in issues:
        if not issue.typeName == 'SubTask':
            print issue.key.ljust(10) + issue.summary


def main():
    args = parse_arguments()

    if args.list_boards and (args.board or args.sprint):
        print "--list-boards cannot be used in conjunction with a board and sprint id. Use one or the other."
        return 1
    elif not args.list_boards and (not args.board or not args.sprint):
        print "Either --list-boards or a board and sprint must be specified"
        return 1

    user = args.user or getpass.getuser()
    password = args.password or getpass.getpass()

    if not user or not password:
        print "Username and password are required"
        return 1


    auth = (user, password)
    options = { 
        'server' : args.server
     }

    try:
        jra = JIRA(options, basic_auth=auth)
        greenhopper = GreenHopper(options, basic_auth=auth)
    except JIRAError as e:
        print "ERROR: %s : %s " % (e.status_code, e.message)
        return 1

    if args.list_boards:
        boards = greenhopper.boards()
        for board in boards:
            print '%s : %s' % (str(board.id).ljust(5), board.name)
    else:
        sprints = greenhopper.sprints(args.board)
        for sprint in sprints:
            if sprint.name == args.sprint:
                completed_issues = greenhopper.completed_issues(args.board, sprint.id)
                print_issues("Completed Issues", completed_issues)
                incompleted_issues = greenhopper.incompleted_issues(args.board, sprint.id)
                print_issues("Incomplete Issues", incompleted_issues)
                stats = gather_stats(completed_issues, jira=jra)
                print stats
    return 0

if __name__ == "__main__":
   sys.exit(main())

