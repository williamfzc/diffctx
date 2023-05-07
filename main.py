import csv
import json
import os
import subprocess
import sys

import openai
import requests
from csvtomd import csv_to_table, md_table
from loguru import logger

from comment import send_comment
from object import FileList

user_dir = "/github/workspace"
support_langs = {"golang", "python"}
csv_result_file = "./output.csv"
json_result_file = "./output.json"
dot_result_file = "./output.dot"


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
            "--outputJson",
            json_result_file,
            "--outputDot",
            dot_result_file,
        ]
    )


def process_with_ai(raw: str) -> str:
    req = f"""
You are a bot for helping code review.
Standard csv report was generated from diff analysis tool.

Here is a csv report below for a specific commit.
Evaluate it and indicate the most important parts which reviewers should care.
Empty report means that there are no dangerous changes.

--- report start ---

{raw}

--- report end ---
"""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": req}]
    )
    return completion.choices[0].message.content


def convert_csv_to_md(csv_file) -> str:
    with open(csv_file, "r") as f:
        markdown_table = csv_to_table(f, ",")
        md_table_raw = md_table(markdown_table)
    return md_table_raw


def process_json(input_json, output_csv):
    with open(input_json, "r") as f:
        json_data = json.load(f)

    file_list = FileList.parse_obj({"files": json_data})

    def format_percentage(numerator, denominator):
        percent = numerator / denominator * 100
        return f"{percent:.2f}% ({numerator}/{denominator})"

    for file in file_list.files:
        file.affectedLinePercentRepr = format_percentage(file.affectedLines, file.totalLines)
        file.affectedFunctionPercentRepr = format_percentage(file.affectedFunctions, file.totalFunctions)
        file.affectedReferencePercentRepr = format_percentage(file.affectedReferences, file.totalReferences)

    file_list.files = sort_files_by_impact(file_list.files)

    cols = [
        "FileName",
        "AffectedLines",
        "AffectedFunctions",
        "AffectedReferences",
    ]
    with open(output_csv, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()

        for file in file_list.files:
            row = {
                cols[0]: file.fileName,
                cols[1]: file.affectedLinePercentRepr,
                cols[2]: file.affectedFunctionPercentRepr,
                cols[3]: file.affectedReferencePercentRepr,
            }
            writer.writerow(row)


def dot_to_svg(dot_file):
    svg_bytes = subprocess.check_output(["dot", "-Tsvg", dot_file])
    return svg_bytes


def sort_files_by_impact(files):
    def sort_key(f):
        return f.affectedLines

    return sorted(files, key=sort_key, reverse=True)


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

    ai_content = "-"
    if not openai_api_key:
        logger.warning("no openai api key found. Use raw data.")
    else:
        logger.info("process with openai")
        openai.api_key = openai_api_key
        ai_content = process_with_ai(content)

    # todo: add to feedback?
    logger.info(f"ai resp: {ai_content}")

    repo_name = os.getenv("GITHUB_REPOSITORY")
    process_json(json_result_file, csv_result_file)
    md_table_raw = convert_csv_to_md(csv_result_file)

    # graph
    svg_bytes = dot_to_svg(dot_result_file)
    # todo: have no idea about how to display this graph in comment without any extra servers

    final_content = f"""
## [DiffCtx](https://github.com/williamfzc/diffctx) Report

{md_table_raw}
"""
    logger.info(f"final comment: {final_content}")

    # feedback
    if not issue_number:
        logger.warning(
            "This action is not triggered by a PR. Will not leave any comments."
        )
        return
    send_comment(repo_token, repo_name, int(issue_number), final_content)

    # # code comments
    # lines = parse_file_as(typing.List[LineStat], pathlib.Path(json_result_file))
    # send_code_comments(repo_token, after_sha, repo_name, int(issue_number), lines)


if __name__ == "__main__":
    main()
