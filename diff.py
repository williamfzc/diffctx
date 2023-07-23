import pathlib

import config
from utils import check_call


def gen_diff(src_dir: str, before_sha: str, after_sha: str, lsif_file: str):
    set_safe_git_dir(src_dir)

    cmds = [
        "srctx",
        "diff",
        "--src",
        src_dir,
        "--before",
        before_sha,
        "--after",
        after_sha,
        "--outputJson",
        config.JSON_RESULT_FILE,
        "--statJson",
        config.STAT_JSON_RESULT_FILE,
    ]
    if not lsif_file:
        lsif_file_loc = pathlib.Path(src_dir) / "dump.lsif"
        scip_file_loc = pathlib.Path(src_dir) / "index.scip"

        if lsif_file_loc.is_file():
            cmds += ["--lsif", str(lsif_file_loc.absolute())]
        elif scip_file_loc.is_file():
            cmds += ["--scip", str(scip_file_loc.absolute())]
        else:
            raise RuntimeError(f"no index file found in {src_dir}")
    else:
        cmds += ["--lsif", lsif_file]

    check_call(cmds)


def set_safe_git_dir(src_dir: str):
    check_call(["git", "config", "--global", "--add", "safe.directory", src_dir])
