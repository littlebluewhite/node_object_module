import datetime

from pydantic import BaseModel

import schemas.control_href_item


class ControlHrefGroupBasic(BaseModel):
    name: str
    tags: list[str] | None = list()


class ControlHrefGroup(ControlHrefGroupBasic):
    id: int
    tags: list[str]

    create_at: datetime.datetime
    update_at: datetime.datetime

    control_href_items: list[schemas.control_href_item.ControlHrefItem] = list()

    class Config:
        orm_mode = True


class ControlHrefGroupCreate(ControlHrefGroupBasic):
    pass


class ControlHrefGroupUpdate(ControlHrefGroupBasic):
    name: str | None = None
    tags: list[str] | None = None


class ControlHrefGroupMultipleUpdate(ControlHrefGroupUpdate):
    id: int
