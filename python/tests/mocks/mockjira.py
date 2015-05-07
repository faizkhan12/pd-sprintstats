import json
import os
from jira import Issue


class JiraObject(object):

    def __init__(self, name, key=None):
        self.name = name
        self.key = key


class JiraIssue(JiraObject):

    def __init__(self, name, key=None):
        super(JiraIssue, self).__init__(name, key)
        self.fields = IssueFields()


class IssueFields(object):

    def __init__(self):
        self.issuetype = None
        self.customfield_10004 = None
        self.created = None
        self.resolutiondate = None


class Jira(object):

    def __init__(self):
        self.issues = []
        self._load_fixtures()

    def _load_fixtures(self):
        files = os.listdir('tests/fixtures/issues')
        for fixture_file in [f for f in files if os.path.splitext(f)[1] == '.json']:
            f = open('tests/fixtures/issues/{0}'.format(fixture_file), 'r')
            issue_dict = json.loads(f.read())
            issue = Issue(None, None, raw=issue_dict)
            self.issues.append(issue)

    def fields(self):
        fields = [
            {'clauseNames': ['chicken', 'Chicken'], 'id': 1},
            {'clauseNames': ['beef', 'Beef'], 'id': 2},
            {'clauseNames': ['pork', 'Pork'], 'id': 3},
            {'clauseNames': ['Story Points'], 'id': 'customfield_10004'}
        ]
        return fields

    def projects(self):
        projects = [
            JiraObject('Project 1', 'PRJ1'),
            JiraObject('Project 2', 'PRJ2'),
            JiraObject('KP1', 'KP2'),
            JiraObject('KeyPrj1', 'KP1'),
        ]
        return projects


class Greenhopper(object):

    def boards(self):
        boards = [
            JiraObject('Board 1'),
            JiraObject('Board 2'),
        ]
        return boards

    def sprints(self, boardid):
        sprints = [
            JiraObject('Sprint 1'),
            JiraObject('Sprint 2')
        ]
        return sprints
