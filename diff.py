from config import user_dir, csv_result_file, json_result_file, dot_result_file
from utils import check_call


def gen_diff(before_sha: str, after_sha: str, lsif_file: str):
    # gen diff
    set_safe_git_dir()

    cmds = [
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
    if lsif_file:
        cmds += ["--lsif", lsif_file]
    check_call(cmds)


def set_safe_git_dir():
    check_call(["git", "config", "--global", "--add", "safe.directory", user_dir])
