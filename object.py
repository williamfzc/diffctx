from pydantic import BaseModel, Field


class ReferenceScope(BaseModel):
    totalRefCount: int
    crossFileRefCount: int
    crossDirRefCount: int

    def is_safe(self):
        return self.totalRefCount == 0 and self.crossFileRefCount == 0 and self.crossDirRefCount == 0


class LineStat(BaseModel):
    fileName: str
    lineNumber: int
    random: bool
    refScope: ReferenceScope = Field(alias="ref")
