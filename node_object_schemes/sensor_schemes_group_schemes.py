from pydantic import BaseModel
from typing import List, Optional


class SensorSchemesGroupBase(BaseModel):
    name: str
    sensor_ids: Optional[List[int]] = None


class SensorSchemesGroup(SensorSchemesGroupBase):
    id: int

    class Config:
        orm_mode = True


class SensorSchemesGroupUpdate(SensorSchemesGroupBase): ...


class SensorSchemesGroupUpdateById(SensorSchemesGroupBase):
    id: int


class SensorSchemesGroupDeleteById(SensorSchemesGroupUpdateById): ...

