import datetime

from pydantic import BaseModel


class DeviceInfoBasic(BaseModel):
    company: str | None = None
    contact_name: str | None = None
    phone_number: str | None = None
    email: str | None = None
    extra_info: str | None = None
    last_maintain_date: datetime.datetime | None = None
    next_maintain_date: datetime.datetime | None = None


class DeviceInfo(DeviceInfoBasic):
    id: int
    node_base_id: int | None = None

    class Config:
        orm_mode = True


class DeviceInfoCreate(DeviceInfoBasic):
    node_base_id: int | None = None


class DeviceInfoUpdate(DeviceInfoBasic):
    company: str | None = None
    contact_name: str | None = None
    phone_number: str | None = None
    email: str | None = None
    node_base_id: int | None = None


class DeviceInfoMultipleUpdate(DeviceInfoUpdate):
    id: int
