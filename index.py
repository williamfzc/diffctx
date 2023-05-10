import os

from loguru import logger

from utils import check_call


def gen_index(lang: str, directory: str, index_command: str):
    current_directory = os.getcwd()
    try:
        os.chdir(directory)

        if index_command:
            logger.info(f"custom index command: {index_command}")
            check_call(index_command.split(" "))

        if lang == "golang":
            gen_golang_index()
        elif lang == "python":
            gen_py_index()
        elif lang == "java":
            gen_java_and_kotlin_index()
        elif lang == "kotlin":
            gen_java_and_kotlin_index()
        else:
            logger.error("no index mapping")
            return
    finally:
        os.chdir(current_directory)


def gen_golang_index():
    check_call(["lsif-go", "-v"])


def gen_java_and_kotlin_index():
    # https://sourcegraph.github.io/scip-java/docs/getting-started.html#run-scip-java-index
    check_call(["scip-java", "index", "--output", "index.scip"])
    # https://github.com/sourcegraph/scip/blob/main/docs/CLI.md
    check_call(["scip", "convert", "--from", "index.scip", "--to", "dump.lsif"])


def gen_py_index():
    check_call(["lsif-py", ".", "--file", "./dump.lsif"])
