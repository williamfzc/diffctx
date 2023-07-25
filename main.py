import csv
import json
import os
import subprocess
import sys
import typing

from csvtomd import csv_to_table, md_table
from loguru import logger

import config
from comment import send_comment
from debug import debug_main
from diff import gen_diff, set_safe_git_dir
from index import gen_index
from object import MetricsResponse as FileList, FileMetrics, StatGlobal


def main():
    # locally run
    # python3 main.py golang HEAD~1 HEAD "" "" "" ./dump.lsif ""
    args = sys.argv[1:]
    lang = args[0]
    before_sha = args[1]
    after_sha = args[2]
    repo_token = args[3]
    issue_number = args[4]
    debug_mode = args[5]
    lsif_file = args[6]
    index_command = args[7]

    if debug_mode:
        logger.warning("in debug mode, start testing")
        debug_main()
        logger.warning("debug mode end")

    # check
    if lang not in config.SUPPORT_LANGS:
        logger.error(f"lang not supported: {lang}, supported: {config.SUPPORT_LANGS}")
        return
    if not before_sha or not after_sha:
        logger.warning("sha empty. Use default.")
        before_sha = "HEAD~1"
        after_sha = "HEAD"
    if not repo_token:
        logger.warning("no repo token provided, run locally")
        config.USER_DIR = "."

    # data prepare
    set_safe_git_dir(config.USER_DIR)
    files = os.listdir(config.USER_DIR)
    logger.info(f"files: {files}")

    if not lsif_file:
        gen_index(lang, config.USER_DIR, index_command)
    gen_diff(config.USER_DIR, before_sha, after_sha, lsif_file)

    repo_name = os.getenv("GITHUB_REPOSITORY")
    file_list = load_index_data()
    summary_data = load_summary_data()

    export_csv_table(summary_data, file_list, config.CSV_RESULT_FILE)
    summary = get_summary(summary_data, file_list)
    md_table_raw = convert_csv_to_md(config.CSV_RESULT_FILE)

    final_content = f"""
## [DiffCtx](https://github.com/williamfzc/diffctx) Report

Start from {before_sha} to {after_sha}.

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


def convert_csv_to_md(csv_file) -> str:
    with open(csv_file, "r") as f:
        markdown_table = csv_to_table(f, ",")
        md_table_raw = md_table(markdown_table)
    return md_table_raw


def export_csv_table(stat: StatGlobal, file_list: typing.List[FileMetrics], output_csv):
    def format_percentage(numerator, denominator):
        percent = numerator / denominator * 100
        return f"{percent:.2f}% ({numerator}/{denominator})"

    for file in file_list:
        file.affectedLinePercentRepr = format_percentage(
            file.impactLineCount, file.totalLineCount
        )
        file.affectedDirectConnectRepr = format_percentage(
            file.impactCount, len(stat.unitMapping)
        )
        file.affectIndirectConnectRepr = format_percentage(
            file.transImpactCount, len(stat.unitMapping)
        )

    file_list = sort_files_by_impact(file_list)

    cols = [
        "File Name",
        "Affected Lines",
        "Direct Impact",
        "Indirect Impact",
    ]
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()

        for file in file_list:
            row = {
                cols[0]: file.fileName,
                cols[1]: file.affectedLinePercentRepr,
                cols[2]: file.affectedDirectConnectRepr,
                cols[3]: file.affectIndirectConnectRepr,
            }
            writer.writerow(row)


def load_index_data() -> typing.List[FileMetrics]:
    with open(config.JSON_RESULT_FILE, "r") as f:
        json_data = json.load(f)

    file_list = FileList.parse_obj({"data": json_data})
    return file_list.data


def load_summary_data() -> StatGlobal:
    with open(config.STAT_JSON_RESULT_FILE, "r") as f:
        json_data = json.load(f)

    return StatGlobal.parse_obj(json_data)


def get_summary(stat: StatGlobal, metrics: typing.List[FileMetrics]) -> str:
    if not metrics:
        return ""

    return (
        f"This PullRequest changes {len(metrics)}/{len(stat.unitMapping)} files, "
        f"possibly impacts {len(stat.impactUnits)}/{len(stat.unitMapping)} files, "
        f"possibly transitive impacts {len(stat.transImpactUnits)}/{len(stat.unitMapping)} files, "
        f"possibly impacts {len(stat.impactEntries)}/{len(stat.entries)} entries."
    )


def dot_to_svg(dot_file):
    svg_bytes = subprocess.check_output(["dot", "-Tsvg", dot_file])
    return svg_bytes


def sort_files_by_impact(
    files: typing.Iterable[FileMetrics],
) -> typing.List[FileMetrics]:
    def sort_key(f: FileMetrics):
        return f.impactLineCount

    return sorted(files, key=sort_key, reverse=True)


if __name__ == "__main__":
    main()
