from pydantic import BaseModel


class DeviceInfoBasic(BaseModel):
    name: str
    company: str
    contact_name: str
    phone_number: str
    email: str
    extra_info: str | None = None


class DeviceInfo(DeviceInfoBasic):
    id: str
    node_base_id: int | None = None

    class Config:
        orm_mode = True


class DeviceInfoCreate(DeviceInfoBasic):
    node_base_id: int | None = None


class DeviceInfoUpdate(DeviceInfoBasic):
    name: str | None = None
    company: str | None = None
    contact_name: str | None = None
    phone_number: str | None = None
    email: str | None = None
    node_base_id: int | None = None


class DeviceInfoMultipleUpdate(DeviceInfoUpdate):
    id: int
