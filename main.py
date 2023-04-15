import os
import subprocess
import sys

import openai
from loguru import logger
from csvtomd import csv_to_table, md_table

from comment import send_comment

user_dir = "/github/workspace"
support_langs = {"golang", "python"}
csv_result_file = "./output.csv"


def gen_index(lang: str):
    set_safe_git_dir()
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
            csv_result_file,
        ]
    )


def process_with_ai(raw: str) -> str:
    req = f"""
You are a bot for helping code review.
Standard csv report was generated from diff analysis tool.
Some descriptions:

- it contains all the influenced lines by this commit
- each row = each line
- RefScope.TotalRefCount: total variable references in this line
- RefScope.CrossFileRefCount: variable references by other files
- RefScope.CrossDirRefCount: variable references by other directories

Here is a csv report below for a specific commit.
Evaluate it and indicate what reviewers should care.
All the file paths should be wrapped with markdown link for navigation.
Empty report means that there are no dangerous changes.

--- report start ---

{raw}

--- report end ---
"""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": req}])
    return completion.choices[0].message.content


def convert_csv_to_md(csv_file) -> str:
    with open(csv_file, 'r') as f:
        markdown_table = csv_to_table(f, ",")
        md_table_raw = md_table(markdown_table)
    return md_table_raw


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

    with open(csv_result_file, encoding="utf-8") as f:
        content = f.read()

    ai_content = ""
    if not openai_api_key:
        logger.warning("no openai api key found. Use raw data.")
    else:
        logger.info("process with openai")
        openai.api_key = openai_api_key
        ai_content = process_with_ai(content)

    repo_name = os.getenv("GITHUB_REPOSITORY")
    md_table_raw = convert_csv_to_md(csv_result_file)

    final_content = f"""
## DiffCtx Feedback

{ai_content} 

<details><summary>Details</summary>

{md_table_raw}

</details>
"""
    logger.info(f"final comment: {final_content}")

    # feedback
    if not issue_number:
        logger.warning("This action is not triggered by a PR. Will not leave any comments.")
        return
    send_comment(repo_token, repo_name, int(issue_number), final_content)


if __name__ == "__main__":
    main()
