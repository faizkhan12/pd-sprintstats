import unittest
from tests.mocks.mockjira import Jira, Greenhopper
from lib.jirahelpers import find_custom_field, find_board, find_sprint, find_project, fetch_subtasks


class TestJiraHelpers(unittest.TestCase):

    def test_can_find_custom_field(self):
        j = Jira()
        field = find_custom_field('chicken', j)
        self.assertIsNotNone(field)

    def test_wont_find_nonexistent_custom_field(self):
        j = Jira()
        field = find_custom_field('not_there', j)
        self.assertIsNone(field)

    def test_can_find_board(self):
        g = Greenhopper()
        b = find_board('Board 1', g)
        self.assertIsNotNone(b)

    def test_wont_find_nonexistent_board(self):
        g = Greenhopper()
        b = find_board('not there', g)
        self.assertIsNone(b)

    def test_find_project_by_name(self):
        j = Jira()
        project = find_project('Project 1', j)
        self.assertIsNotNone(project)

    def test_find_project_by_key(self):
        j = Jira()
        project = find_project('PRJ1', j)
        self.assertIsNotNone(project)

    def test_wont_find_nonexistent_project(self):
        j = Jira()
        project = find_project('Not There', j)
        self.assertIsNone(project)

    def test_find_project_matches_key_first(self):
        j = Jira()
        project = find_project('KP1', j)
        self.assertEquals(project.key, 'KP1')
