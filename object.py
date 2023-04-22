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
