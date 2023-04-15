import os
import subprocess
import sys
from loguru import logger

from comment import send_comment

user_dir = "/github/workspace"
support_langs = {"golang", "python"}


def gen_index(lang: str):
    files = os.listdir(user_dir)
    logger.info(f"files: {files}")

    if lang == "golang":
        gen_golang_index()
    elif lang == "python":
        gen_py_index()
    else:
        logger.error("no index mapping")
        return


def gen_golang_index():
    _check_call(["lsif-go", "-v"])


def gen_py_index():
    _check_call(["lsif-py", ".", "--file", "./dump.lsif"])


def _check_call(commands: list):
    subprocess.check_call(commands, cwd=user_dir)


def set_safe_git_dir():
    _check_call(["git", "config", "--global", "--add", "safe.directory", user_dir])


def gen_diff(before_sha: str, after_sha: str):
    # gen diff
    set_safe_git_dir()
    _check_call(
        [
            "srctx",
            "diff",
            "--src",
            user_dir,
            "--before",
            before_sha,
            "--after",
            after_sha,
        ]
    )


def main():
    args = sys.argv[1:]
    lang = args[0]
    before_sha = args[1]
    after_sha = args[2]
    repo_token = args[3]
    issue_id = args[4]

    # check
    if lang not in support_langs:
        logger.error(f"lang not supported: {lang}, supported: {support_langs}")
        return
    if not before_sha or not after_sha:
        logger.warning("sha empty. Use default.")
        before_sha = "HEAD~1"
        after_sha = "HEAD"
    if not repo_token:
        logger.error("no repo token provided")
        return

    # data prepare
    gen_index(lang)
    gen_diff(before_sha, after_sha)

    files = os.listdir(".")

    # feedback
    repo_name = os.getenv("GITHUB_REPOSITORY")
    send_comment(repo_token, repo_name, int(issue_id), f"hi from github action: {files}")


if __name__ == "__main__":
    main()
