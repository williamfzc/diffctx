import os
import subprocess
import typing

from loguru import logger


def check_call(commands: typing.Union[str, list]):
    logger.info(f"check calling: {commands}")
    if isinstance(commands, str):
        subprocess.check_call(commands, env=os.environ, shell=True)
    else:
        subprocess.check_call(commands, env=os.environ)
