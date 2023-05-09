import subprocess

from config import user_dir


def check_call(commands: list):
    subprocess.check_call(commands, cwd=user_dir)
