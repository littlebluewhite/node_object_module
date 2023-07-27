import datetime

from pydantic import BaseModel


class ControlHrefItemBasic(BaseModel):
    name: str | None = None
    control_data: str | None = None
    color: str | None = None
    control_href_group_id: int | None = None
    tags: list[str] = list()


class ControlHrefItem(ControlHrefItemBasic):
    id: int
    tags: list[str] | None = list()

    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class ControlHrefItemCreate(ControlHrefItemBasic):
    tags: list[str] | None = list()


class ControlHrefItemUpdate(ControlHrefItemBasic):
    tags: list[str] | None = None


class ControlHrefItemMultipleUpdate(ControlHrefItemUpdate):
    id: int
