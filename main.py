import os
import subprocess
import sys
from loguru import logger

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


def main():
    args = sys.argv[1:]
    logger.info(f"args: {args}")
    lang = args[0]
    before_sha = args[1]
    after_sha = args[2]
    # check
    if lang not in support_langs:
        logger.error(f"lang not supported: {lang}, supported: {support_langs}")
        return
    if not before_sha or not after_sha:
        logger.warning("sha empty. Use default.")
        before_sha = "HEAD~1"
        after_sha = "HEAD"

    gen_index(lang)
    # gen diff
    set_safe_git_dir()
    _check_call(["srctx", "diff",
                 "--src", user_dir,
                 "--before", before_sha,
                 "--after", after_sha])


if __name__ == "__main__":
    main()
