import os
import subprocess
import sys
from loguru import logger

user_dir = "/github/workspace"
support_langs = {"golang", "python"}


def gen_index(lang: str):
    if lang not in support_langs:
        logger.error(f"lang not supported: {lang}, supported: {support_langs}")
        return

    files = os.listdir(user_dir)
    logger.info(f"files: {files}")

    if lang == "golang":
        gen_golang_index()
    elif lang == "python":
        gen_py_index()
    else:
        logger.error("no index mapping")
        return
    _check_call(["srctx", "diff"])


def gen_golang_index():
    _check_call(["lsif-go", "-v"])


def gen_py_index():
    _check_call(["lsif-py", "."])


def _check_call(commands: list):
    subprocess.check_call(commands, cwd=user_dir)


def main():
    args = sys.argv[1:]
    logger.info(f"args: {args}")
    lang = args[0]
    gen_index(lang)


if __name__ == "__main__":
    main()
