import unittest
from tests.mocks.mockjira import Jira, Greenhopper, JiraIssue, JiraObject
import imp
sprintstats = imp.load_source('sprintstats', 'sprintstats')
from sprintstats import sum_story_points, calculate_cycle_times


class TestSprintStats(unittest.TestCase):

    def _make_issues(self, num_issues, points_per_issue, issue_type):
        issues = []
        for i in range(num_issues):
            issue = JiraIssue('TS-{0}'.format(i), 'Test Issue {0}'.format(1))
            issue.fields.customfield_10004 = points_per_issue
            issue.fields.issuetype = JiraObject(issue_type)
            issues.append(issue)
        return issues

    def test_sum_story_points_all_issues_scored(self):
        j = Jira()
        num_issues = 5
        points = 5
        issues = self._make_issues(num_issues, points, 'Story')
        sum_of_points = sum_story_points(issues, j)
        self.assertEquals(sum_of_points, num_issues * points)

    def test_sum_story_points_excludes_sub_tasks(self):
        j = Jira()
        issues = self._make_issues(1, 10, 'Story')
        issues += self._make_issues(1, 10, 'Sub-task')
        sum_of_points = sum_story_points(issues, j)
        self.assertEquals(sum_of_points, 10)

    def test_sum_story_points_handles_empty_list(self):
        j = Jira()
        issues = []
        points = sum_story_points(issues, j)
        self.assertEquals(points, 0)

    def test_sum_story_points_applies_default_points(self):
        j = Jira()
        num_issues = 10
        issues = self._make_issues(10, None, 'Story')
        default_points = 10
        points = sum_story_points(issues, j, default_points=default_points)
        self.assertEquals(points, num_issues * default_points)

    def test_calculate_cycle_times(self):
        issues = self._make_issues(2, 1, 'Story')
        i1 = issues[0]
        i1.fields.created = '2015-05-01T12:00:00.000-0000'
        i1.fields.resolutiondate = '2015-05-03T12:00:00.000-0000'

        i2 = issues[1]
        i2.fields.created = '2015-01-01T12:00:00.000-0000'
        i2.fields.resolutiondate = '2015-01-05T12:00:00.000-0000'

        times = calculate_cycle_times(issues)
        self.assertEquals(times['min_cycle_time'], 2)
        self.assertEquals(times['max_cycle_time'], 4)
        self.assertEquals(times['average_cycle_time'], 3)
        self.assertEquals(times['cycle_time_stddev'], 1.0)

    def test_calculate_cycle_times_handles_empty_list(self):
        issues = []
        times = calculate_cycle_times(issues)
        self.assertEquals(times['min_cycle_time'], -1)
        self.assertEquals(times['max_cycle_time'], -1)
        self.assertEquals(times['average_cycle_time'], -1)
        self.assertEquals(times['cycle_time_stddev'], -1)
