from lib.output import dot

def find_custom_field(field_name, jira):
    fields = jira.fields()
    for f in fields:
        if field_name in f['clauseNames']:
            return f

def find_board(board_name, greenhopper):
    boards = [b for b in greenhopper.boards() if b.name == board_name]
    if len(boards):
        return boards[0]
    return None


def find_sprint(sprint_name, board, greenhopper):
    sprints = [s for s in greenhopper.sprints(
        board.id) if s.name == sprint_name]
    if len(sprints):
        return sprints[0]
    return None


def find_project(project_name_or_key, jira):
    projects = [p for p in jira.projects()
                if p.name == project_name_or_key
                or p.key == project_name_or_key]
    if len(projects):
        return projects[0]
    return None

def fetch_subtasks(iss, jira):
    subtasks = []
    if hasattr(iss, 'fields') and hasattr(iss.fields, 'subtasks'):
        for subt in iss.fields.subtasks:
            dot()
            subt = jira.issue(subt.key, expand='changelog')
            subtasks.append(subt)
            subtasks = subtasks + fetch_subtasks(subt, jira)
    return subtasks

