import os

from loguru import logger

from diff import set_safe_git_dir
from config import user_dir
from utils import check_call


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
    check_call(["lsif-go", "-v"])


def gen_java_and_kotlin_index():
    # https://sourcegraph.github.io/scip-java/docs/getting-started.html#run-scip-java-index
    check_call(["scip-java", "index", "--output", "index.scip"])
    # https://github.com/sourcegraph/scip/blob/main/docs/CLI.md
    check_call(["scip", "convert", "--from", "index.scip", "--to", "dump.lsif"])


def gen_py_index():
    check_call(["lsif-py", ".", "--file", "./dump.lsif"])
