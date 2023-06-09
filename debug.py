import os

from diff import gen_diff
from index import gen_index
from utils import check_call
import shutil


def debug_main():
    # pull some repos for test
    check_call(["git", "clone", "--depth=2", "https://github.com/gin-gonic/gin.git"])
    check_call(["git", "clone", "--depth=2", "https://github.com/google/guava"])

    gen_index("golang", "gin", "")
    gen_index("java", "guava", "")

    os.chdir("gin")
    gen_diff("HEAD~1", "HEAD", "")
    os.chdir("..")

    os.chdir("guava")
    gen_diff("HEAD~1", "HEAD", "")
    os.chdir("..")

    # clean up
    shutil.rmtree("gin")
    shutil.rmtree("guava")
