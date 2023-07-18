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
            return

        if lang == "golang":
            gen_golang_index()
        elif lang == "python":
            gen_py_index()
        elif lang == "java":
            gen_java_and_kotlin_index()
        elif lang == "kotlin":
            gen_java_and_kotlin_index()
        elif lang == "node":
            gen_node_index()
        else:
            raise RuntimeError(f"lang {lang} not support")
    finally:
        os.chdir(current_directory)


def gen_golang_index():
    check_call(["lsif-go", "-v"])


def gen_java_and_kotlin_index():
    # https://sourcegraph.github.io/scip-java/docs/getting-started.html#run-scip-java-index
    check_call(["scip-java", "index", "--output", "index.scip"])


def gen_py_index():
    check_call(["scip-python", "index", ".", "--project-name", "srctx"])


def gen_node_index():
    check_call(
        [
            "lsif",
            "tsc",
            "-p",
            "./tsconfig.json",
            "--package",
            "./package.json",
            "--stdout",
        ]
    )
