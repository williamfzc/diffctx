import os
import subprocess
from loguru import logger


def check_call(commands: list):
    logger.info(f"check calling: {commands}")
    subprocess.check_call(commands, env=os.environ)
