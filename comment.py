from github import Github
from loguru import logger


def send_comment(token: str, repo_id: str, issue_id: int, content: str):
    logger.info(f"send comment to {repo_id}, issue id: {issue_id}")
    g = Github(token)
    repo = g.get_repo(repo_id)
    pr = repo.get_pull(issue_id)
    pr.create_issue_comment(content)
