import typing

from pydantic import BaseModel


class FileMetrics(BaseModel):
    fileName: str
    unitName: str
    directConnectCount: int
    inDirectConnectCount: int
    totalUnitCount: int
    affectedEntries: int
    totalEntriesCount: int
    affectedLineCount: int
    totalLineCount: int

    # extras
    affectedLinePercentRepr: str = ""
    affectedDirectConnectRepr: str = ""
    affectIndirectConnectRepr: str = ""


class MetricsResponse(BaseModel):
    data: typing.List[FileMetrics]
