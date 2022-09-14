import datetime

from pydantic import BaseModel


class ControlHrefItemBasic(BaseModel):
    name: str
    control_data: str
    color: str | None = None
    control_href_group_id: int | None = None
    tags: list[str] = list()


class ControlHrefItem(ControlHrefItemBasic):
    id: str
    tags: list[str]

    create_at: datetime.datetime
    update_at: datetime.datetime

    class Config:
        orm_mode = True


class ControlHrefItemCreate(ControlHrefItemBasic):
    pass


class ControlHrefItemUpdate(ControlHrefItemBasic):
    name: str | None = None
    control_data: str | None = None
    tags: list[str] | None = None


class ControlHrefItemMultipleUpdate(ControlHrefItemUpdate):
    id: int
