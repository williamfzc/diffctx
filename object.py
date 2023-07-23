import typing

from pydantic import BaseModel


class FileMetrics(BaseModel):
    fileName: str
    unitName: str
    impactCount: int
    transImpactCount: int
    impactEntries: int
    impactLineCount: int
    totalLineCount: int

    # extras
    affectedLinePercentRepr: str = ""
    affectedDirectConnectRepr: str = ""
    affectIndirectConnectRepr: str = ""


class MetricsResponse(BaseModel):
    data: typing.List[FileMetrics]


class StatGlobal(BaseModel):
    unitLevel: str
    unitMapping: typing.Dict[str, int] = dict()
    impactUnits: typing.List[int] = []
    transImpactUnits: typing.List[int] = []
    entries: typing.List[int] = []
    impactEntries: typing.List[int] = []
