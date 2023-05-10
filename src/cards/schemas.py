from typing import Optional, List

from pydantic import BaseModel


class ArcaneBaseSchema(BaseModel):
    id: int
    type: str
    name: str
    slug: str
    card: str
    brief: str
    general: Optional[str] = None
    personal_condition: Optional[str] = None
    deep: Optional[str] = None
    career: Optional[str] = None
    finances: Optional[str] = None
    relations: Optional[str] = None
    upside_down: Optional[str] = None
    combination: Optional[str] = None
    archetypal: Optional[str] = None
    health: Optional[str] = None
    remarks: Optional[str] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ArcanesResponse(BaseModel):
    status: str
    results: int
    notes: List[ArcaneBaseSchema]
