#!/usr/bin/env python
from jira.client import JIRA
from jira.client import GreenHopper
from jira import JIRAError
from ConfigParser import SafeConfigParser
import dateutil.parser
import argparse
import getpass
import sys
import numpy

def parse_config():
    settings = {}
    parser = SafeConfigParser()
    parser.read('config.cfg')
    if parser.has_section('default'):
       settings = dict(parser.items('default'))
    return settings

def parse_arguments():
    parser = argparse.ArgumentParser(description='Gather some statistics about a JIRA sprint')
    parser.add_argument('--user', '-u', metavar='USER',  help='The JIRA user name to used for auth. If omitted the current user name will be used.')
    parser.add_argument('--password','-p', metavar='PASSWORD',  help='The JIRA password to be used for auth. If omitted you will be prompted.')
    parser.add_argument('-P', action='store_true', dest='prompt', help='Prompt for password.')
    parser.add_argument('--list-boards', '-l',  action='store_true', help='When supplied, a list of RapidBoards and their associated IDs are displayed')
    parser.add_argument('--server', '-s', metavar='SERVER')
    parser.add_argument('--board', '-b', nargs='?', help='The id of the rapidboard that houses the sprint on which you want to gather stats. (Use --list-boards to find it')
    parser.add_argument('--sprint', '-t',  nargs='?', help='The name of the sprint on which to produce the stats')

    args = parser.parse_args()
    return args

def find_custom_field(field_name, jira):
    fields = jira.fields()
    for f in fields:
        if field_name in f['clauseNames']:
            return f

def calculate_velocity(issues, jira):
    velocity = 0
    story_point_field = find_custom_field('Story Points', jira)
    if not story_point_field:
        raise Exception('Could not find the story points custom field for this jira instance')

    for issue in issues:
        sys.stdout.write('.'); sys.stdout.flush()
        if issue.typeName != 'SubTask':
            iss = jira.issue(issue.key)
            velocity += getattr(iss.fields, story_point_field['id'])
    return velocity

def calculate_cycle_times(issues, jira):
    times = []
    for issue in issues:
        sys.stdout.write('.'); sys.stdout.flush()
        if issue.typeName != 'SubTask':
            iss = jira.issue(issue.key)
            open_time = dateutil.parser.parse(iss.fields.created)
            close_time = dateutil.parser.parse(iss.fields.resolutiondate)
            cycle_time = (close_time - open_time).days
            times.append(cycle_time)
    arr = numpy.array(times)
    average_cycle = numpy.mean(arr)
    std_deviation = numpy.std(arr)
    ret = {
        'min_cycle_time' : min(times),
        'max_cycle_time' : max(times),
        'average_cycle_time' : average_cycle,
        'cycle_time_stddev' : std_deviation
    }
    return ret

def gather_stats(issues, jira):
    stats = {}
    velocity = calculate_velocity(issues, jira)
    stats['velocity'] = velocity
    stats.update(calculate_cycle_times(issues, jira))
    return stats

def print_issues(title, issues):
    print title
    print '=' * len(title)
    for issue in issues:
        if not issue.typeName == 'SubTask':
            print issue.key.ljust(10) + issue.summary

def print_stats(title, stats):
    print title
    print '=' * len(title)
    for k, v in stats.iteritems():
        print k.ljust(20) + ':' + str(v)

def find_board_id(board_name, greenhopper):
    boards = greenhopper.boards()
    for board in boards:
        if board.name == board_name:
            return board.id
    return None

def main():
    config = parse_config()
    args = parse_arguments()

    if args.list_boards and (args.board or args.sprint):
        print '--list-boards cannot be used in conjunction with a board and sprint id. Use one or the other.'
        return 1
    elif not args.list_boards and (not args.board or not args.sprint):
        print 'Either --list-boards or a board and sprint must be specified'
        return 1

    user = args.user or config['user'] or getpass.getuser()
    password = args.password or config['password'] or (args.prompt and getpass.getpass())

    if not user or not password:
        print 'Username and password are required'
        return 1

    auth = (user, password)
    options = {
        'server' : args.server or config['server'] or 'https://jira.atlassian.com'
    }

    try:
        jra = JIRA(options, basic_auth=auth)
        greenhopper = GreenHopper(options, basic_auth=auth)
    except JIRAError as e:
        print 'ERROR: %s : %s ' % (e.status_code, e.message)
        return 1

    if args.list_boards:
        boards = greenhopper.boards()
        for board in boards:
            print '%s : %s' % (str(board.id).ljust(5), board.name)
    else:
        if not args.board.isdigit():
            args.board = find_board_id(args.board, greenhopper)
            if not args.board:
                print "Board not found"
                return 1
        sprints = greenhopper.sprints(args.board)
        for sprint in sprints:
            if sprint.name == args.sprint:
                completed_issues = greenhopper.completed_issues(args.board, sprint.id)
                print_issues('Completed Issues', completed_issues)
                incompleted_issues = greenhopper.incompleted_issues(args.board, sprint.id)
                sys.stdout.write('\n')
                print_issues('Incomplete Issues', incompleted_issues)
                stats = gather_stats(completed_issues, jira=jra)
                sys.stdout.write('\n')
                print_stats("Sprint Statistics", stats)
    return 0

if __name__ == '__main__':
   sys.exit(main())

