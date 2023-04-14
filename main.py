import os
import subprocess
from loguru import logger

user_dir = "/github/workspace"


def gen_index():
    files = os.listdir(user_dir)
    logger.info(f"files: {files}")
    _check_call(["bash", "./create_and_diff.sh"])


def _check_call(commands: list):
    subprocess.check_call(commands, cwd=user_dir)


def main():
    gen_index()


if __name__ == "__main__":
    main()
