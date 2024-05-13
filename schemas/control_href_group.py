import datetime

from pydantic import BaseModel

import schemas.control_href_item


class ControlHrefGroupBasic(BaseModel):
    uid: str
    tags: list[str] | None = list()


class ControlHrefGroup(ControlHrefGroupBasic):
    id: int
    tags: list[str]

    created_at: datetime.datetime
    updated_at: datetime.datetime

    control_href_items: list[schemas.control_href_item.ControlHrefItem] = list()

    class Config:
        orm_mode = True


class ControlHrefGroupCreate(ControlHrefGroupBasic):
    pass


class ControlHrefGroupUpdate(ControlHrefGroupBasic):
    uid: str | None = None
    tags: list[str] | None = None


class ControlHrefGroupMultipleUpdate(ControlHrefGroupUpdate):
    id: int
