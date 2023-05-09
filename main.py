import csv
import json
import os
import subprocess
import sys

import openai
from csvtomd import csv_to_table, md_table
from loguru import logger

from ai import process_with_ai
from comment import send_comment
from config import support_langs, csv_result_file, json_result_file, dot_result_file
from diff import gen_diff
from index import gen_index
from object import FileList


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
    diff_desc = f"Start from {before_sha} to {after_sha}."
    summary = get_summary(json_result_file)
    md_table_raw = convert_csv_to_md(csv_result_file)

    # graph
    svg_bytes = dot_to_svg(dot_result_file)
    # todo: have no idea about how to display this graph in comment without any extra servers

    final_content = f"""
## [DiffCtx](https://github.com/williamfzc/diffctx) Report

{diff_desc}

{summary}

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
        file.affectedLinePercentRepr = format_percentage(
            file.affectedLines, file.totalLines
        )
        file.affectedFunctionPercentRepr = format_percentage(
            file.affectedFunctions, file.totalFunctions
        )
        file.affectedReferencePercentRepr = format_percentage(
            file.affectedReferences, file.totalReferences
        )

    file_list.files = sort_files_by_impact(file_list.files)

    cols = [
        "FileName",
        "AffectedLines",
        "AffectedFunctions",
        "AffectedReferences",
    ]
    with open(output_csv, "w", newline="") as f:
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


def get_summary(input_json) -> str:
    with open(input_json, "r") as f:
        json_data = json.load(f)

    file_list = FileList.parse_obj({"files": json_data})

    affected_files = len(file_list.files)
    affected_lines = sum([each.affectedLines for each in file_list.files])
    affected_functions = sum([each.affectedFunctions for each in file_list.files])
    affected_refs = sum([each.affectedReferences for each in file_list.files])

    return (
        f"This commit directly influences {affected_files} files, "
        f"{affected_lines} lines, "
        f"{affected_functions} functions. "
        f"Indirectly influences {affected_refs} functions. "
    )


def dot_to_svg(dot_file):
    svg_bytes = subprocess.check_output(["dot", "-Tsvg", dot_file])
    return svg_bytes


def sort_files_by_impact(files):
    def sort_key(f):
        return f.affectedLines

    return sorted(files, key=sort_key, reverse=True)


if __name__ == "__main__":
    main()
