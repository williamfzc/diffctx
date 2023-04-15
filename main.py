import os
import subprocess
import sys

import openai
from loguru import logger

from comment import send_comment

user_dir = "/github/workspace"
support_langs = {"golang", "python"}
csv_result = "./output.csv"


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
            "--outputCsv",
            csv_result,
        ]
    )


def process_with_ai(raw: str) -> str:
    req = f"""
You are a bot for helping code review.
This csv report was generated from diff analysis tool.
Some descriptions:

- it contains all the influenced lines by this commit
- each row = each line
- RefScope.TotalRefCount: total variable references in this line
- RefScope.CrossFileRefCount: variable references by other files
- RefScope.CrossDirRefCount: variable references by other directories

Help me evaluate it and indicate what reviewers should care:

{raw}
"""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": req}])
    return completion.choices[0].message.content


def main():
    args = sys.argv[1:]
    lang = args[0]
    before_sha = args[1]
    after_sha = args[2]
    repo_token = args[3]
    issue_number = args[4]
    openai_api_key = args[5]

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

    with open(csv_result, encoding="utf-8") as f:
        content = f.read()

    if not openai_api_key:
        logger.warning("no openai api key found. Use raw data.")
    else:
        logger.info("process with openai")
        openai.api_key = openai_api_key
        content = process_with_ai(content)
    logger.info(f"reply content: {content}")

    # feedback
    if not issue_number:
        logger.warning("This action is not triggered by a PR. Will not leave any comments.")
        return

    repo_name = os.getenv("GITHUB_REPOSITORY")
    send_comment(repo_token, repo_name, int(issue_number), f"""
## DiffCtx Feedback

{content} 
""")


if __name__ == "__main__":
    main()
