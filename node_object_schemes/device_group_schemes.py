from typing import Optional, List

from pydantic import BaseModel


class DeviceGroupBase(BaseModel):
    name: str
    device_ids: List[int]


class DeviceGroup(DeviceGroupBase):
    id: int

    class Config:
        orm_mode = True


class DeviceGroupUpdate(DeviceGroupBase): ...


class DeviceGroupUpdateById(DeviceGroupBase):
    id: int


class DeviceGroupDeleteById(DeviceGroupUpdateById):...