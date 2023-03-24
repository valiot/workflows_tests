from typing import Dict, Union
import json
import os
# External imports
from github import Github, Repository


def comment_pull_request(github_token: str, event_path: str, file_name: str) -> None:
    """Comment the PR from a given `template` of comment.

    Args:
    ------
        - github_token (str): Token to access to the Github API endpoint
        - event_path (str): The path to the event received
        - filename (str): File from where we'd take the information for the comment
    """
    github: Github = Github(github_token)
    # Read the event as a json input
    with open(event_path, "r", encoding="utf-8") as event_info:
        event: Dict[str, dict] = json.load(event_info)
    # From here, obtain needed information
    branch_label = event['pull_request']['head']['label']
    branch_name = branch_label.split(':')[-1]
    # Obtain the repository from the event path
    repo: Repository = github.get_repo(event['repository']['full_name'])
    # Obtain the PR from the repo. You'd get the correct PR with the branch_label
    pr = repo.get_pulls(state='open', sort='created', head=branch_label)[0]

    # Load the comment template
    with open(file_name, 'r', encoding="utf8") as file_template:
        comment_template = file_template.read()

    # Structure the comment information in the template
    comment = comment_template.format({
        "pull_id": pr.number,
        "branch_name": branch_name
    })

    # Check if this pull request already has this comment
    pr_comments = [comment.body for comment in pr.get_issue_comments()]
    if comment in pr_comments:
        print('This pull request already has this comment.')
        return

    # If the comment is new, that is, the comment is not in the PR comments, then send it
    pr.create_issue_comment(comment)
    return


if __name__ == '__main__':
    git_token: Union[str, None] = os.environ.get('GITHUB_TOKEN')
    git_event_path: Union[str, None] = os.environ.get('GITHUB_EVENT_PATH')
    comment_filename: Union[str, None] = os.environ.get('FILENAME')
    # Check if you have one of these variables
    if not git_token:
        raise ValueError("The github token is missing, please add it.")
    if not git_event_path:
        raise ValueError("The github event path is missing, please add it.")
    if not comment_filename:
        raise ValueError(
            "The filename with the comment template is missing, please add it.")
    # Call the function to generate the comment
    comment_pull_request(git_token, git_event_path, comment_filename)
