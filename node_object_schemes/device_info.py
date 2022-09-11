from pydantic import BaseModel


class DeviceInfoBasic(BaseModel):
    name: str
    company: str
    contact_name: str
    phone_number: str
    email: str


class DeviceInfo(DeviceInfoBasic):
    id: str

    class Config:
        orm_mode = True


class DeviceInfoCreate(DeviceInfoBasic):
    pass


class DeviceInfoUpdate(DeviceInfoBasic):
    name: str | None = None
    company: str | None = None
    contact_name: str | None = None
    phone_number: str | None = None
    email: str | None = None


class DeviceInfoMultipleUpdate(DeviceInfoUpdate):
    id: int
