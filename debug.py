import os
import pathlib

import config
from diff import gen_diff
from index import gen_index
from utils import check_call
import shutil


def debug_main():
    # clone junit4 repository
    check_call(
        ["git", "clone", "--depth=2", "https://github.com/junit-team/junit4.git"]
    )
    junit4_dir = pathlib.Path(config.USER_DIR) / "junit4"
    gen_index(
        "java",
        junit4_dir.as_posix(),
        "scip-java index -- "
        "package -DskipTests "
        "--batch-mode "
        "--errors "
        "--settings .github/workflows/settings.xml",
    )
    os.chdir(junit4_dir)
    gen_diff(junit4_dir.as_posix(), "HEAD~1", "HEAD", "")
    os.chdir(config.USER_DIR)
    shutil.rmtree(junit4_dir)

    # clone gin repository
    check_call(["git", "clone", "--depth=2", "https://github.com/gin-gonic/gin.git"])
    gin_dir = pathlib.Path(config.USER_DIR) / "gin"
    os.chdir(gin_dir)
    gen_index("golang", gin_dir.as_posix(), "")
    gen_diff(gin_dir.as_posix(), "HEAD~1", "HEAD", "")
    os.chdir(config.USER_DIR)
    shutil.rmtree(gin_dir)

    # clone requests repository
    check_call(["git", "clone", "--depth=2", "https://github.com/psf/requests.git"])
    requests_dir = pathlib.Path(config.USER_DIR) / "requests"
    os.chdir(requests_dir)
    gen_index("python", requests_dir.as_posix(), "")
    gen_diff(requests_dir.as_posix(), "HEAD~1", "HEAD", "")
    os.chdir(config.USER_DIR)
    shutil.rmtree(requests_dir)
