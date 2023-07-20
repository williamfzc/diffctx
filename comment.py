from github import Github
from loguru import logger


def send_comment(token: str, repo_id: str, issue_number: int, content: str):
    logger.info(f"send comment to {repo_id}, issue id: {issue_number}")
    g = Github(token)
    repo = g.get_repo(repo_id)
    pr = repo.get_pull(issue_number)
    comments = pr.get_issue_comments()
    for each in comments:
        if "DiffCtx Report" in each.body:
            logger.info(f"found an existed comment: {each.id}, edit directly")
            each.edit(content)
            return

    # no existed comment
    pr.create_issue_comment(content)
