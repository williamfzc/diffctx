import config
from utils import check_call


def gen_diff(before_sha: str, after_sha: str, lsif_file: str):
    # gen diff
    set_safe_git_dir()

    cmds = [
        "srctx",
        "diff",
        "--src",
        config.USER_DIR,
        "--before",
        before_sha,
        "--after",
        after_sha,
        "--outputJson",
        config.JSON_RESULT_FILE,
        "--outputCsv",
        config.CSV_RESULT_FILE,
    ]
    if lsif_file:
        cmds += ["--lsif", lsif_file]
    check_call(cmds)


def set_safe_git_dir():
    check_call(
        ["git", "config", "--global", "--add", "safe.directory", config.USER_DIR]
    )
