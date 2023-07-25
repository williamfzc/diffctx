import os
import subprocess
import typing

from loguru import logger


def check_call(commands: typing.Union[str, list]):
    logger.info(f"check calling: {commands}")
    if isinstance(commands, str):
        # for https://github.com/orgs/community/discussions/25738
        commands = "JAVA_HOME=/usr/lib/jvm/java-8-openjdk" + " " + commands
        subprocess.check_call(commands, env=os.environ, shell=True)
    else:
        subprocess.check_call(commands, env=os.environ)
