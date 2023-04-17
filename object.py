from pydantic import BaseModel


class FileScope(BaseModel):
    fileName: str
    lineNumber: int
    random: bool


class ReferenceScope(BaseModel):
    totalRefCount: int
    crossFileRefCount: int
    crossDirRefCount: int

    def is_safe(self):
        return self.totalRefCount == 0 and self.crossFileRefCount == 0 and self.crossDirRefCount == 0


class LineStat(BaseModel):
    fileScope: FileScope
    refScope: ReferenceScope
