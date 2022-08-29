from typing import Optional

from pydantic import BaseModel


class DeviceInfoBase(BaseModel):
    company: str  # 設備廠商
    owner_name: Optional[str] = None  # 廠商聯絡人
    phone_number: Optional[int] = None  # 廠商電話
    email: Optional[str] = None  # 廠商Mail


class DeviceInfo(DeviceInfoBase):
    id: int

    class Config:
        orm_mode = True


class DeviceInfoUpdate(DeviceInfoBase):...


class DeviceInfoUpdateById(DeviceInfoBase):
    id: int


class DeviceInfoDeleteById(DeviceInfoUpdateById):...
