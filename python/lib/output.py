from __future__ import print_function
import sys

def dot():
    if sys.stderr.isatty():
        sys.stderr.write('.')
        sys.stderr.flush()

def output_issues(title, issues):
    print (title)
    print ('=' * len(title))
    for issue in [i for i in issues if i.typeName != 'SubTask']:
        print (issue.key.ljust(10) + issue.summary)
    print('\r')


def output_stats(title, stats, indent=0):
    print('\t' * indent + title)
    print('\t' * indent + '=' * len(title))
    for k, v in sorted(stats.iteritems()):
        if isinstance(v, dict):
            output_stats(k, v, indent + 1)
        else:
            print('\t' * indent + k.ljust(20) + ':' + str(v))
    print('\r')



