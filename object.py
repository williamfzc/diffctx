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


class FileVertex(BaseModel):
    fileName: str
    affectedLinePercent: float
    affectedFunctionPercent: float
    affectedReferencePercent: float

    affectedLinePercentRepr: str = ""
    affectedFunctionPercentRepr: str = ""
    affectedReferencePercentRepr: str = ""

    affectedLines: int
    totalLines: int

    affectedFunctions: int
    totalFunctions: int

    affectedReferences: int
    totalReferences: int


class FileList(BaseModel):
    files: typing.List[FileVertex]
