import typing

from pydantic import BaseModel, Field


class ReferenceScope(BaseModel):
    totalRefCount: int
    crossFileRefCount: int
    crossDirRefCount: int


class FuncReferenceScope(BaseModel):
    totalFuncRefCount: int
    crossFuncFileRefCount: int
    crossFuncDirRefCount: int


class LineStat(BaseModel):
    fileName: str
    lineNumber: int
    refScope: ReferenceScope = Field(alias="ref")
    funcScope: FuncReferenceScope = Field(alias="funcRef")


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
