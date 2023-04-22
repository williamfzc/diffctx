import typing

from github import Github
from github3 import GitHub as Github3
from github3.pulls import PullRequest
from github3.repos import Repository
from loguru import logger

from object import LineStat


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


def send_code_comments(
    token: str,
    commit_id: str,
    repo_id: str,
    issue_number: int,
    lines: typing.List[LineStat],
):
    gg = Github3(token=token)
    owner, cur_repo = repo_id.split("/")
    repo: Repository = gg.repository(owner, cur_repo)

    logger.info(f"target commit: {commit_id}")
    pr: PullRequest = repo.pull_request(issue_number)
    logger.info(f"target pr: {issue_number}")

    for each_line in lines:
        if each_line.refScope.crossFileRefCount > 0:
            logger.info(
                f"leave comment in {each_line.fileName} L{each_line.lineNumber}"
            )
            # todo: 443 failed
            # https://github.com/PyGithub/PyGithub/issues/2501

            # pr.create_review_comment(
            #     f"[diffctx] cross file reference: {each_line.refScope.crossFileRefCount}",
            #     commit_id,
            #     each_line.fileName,
            #     each_line.lineNumber,
            # )
