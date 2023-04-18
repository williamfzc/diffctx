import pathlib
import typing
from pydantic import parse_file_as

from object import LineStat


def test_parse_file_as():
    parse_file_as(typing.List[LineStat], pathlib.Path("./output.json"))
