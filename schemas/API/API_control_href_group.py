import datetime

from pydantic import BaseModel
from schemas.control_href_group import ControlHrefGroupBasic


class APIControlHrefItemBasic(BaseModel):
    name: str
    control_data: str
    color: str | None = None
    tags: list[str] = list()


class APIControlHrefGroupSimple(BaseModel):
    id: int
    uid: str | None
    name: str | None


class APIControlHrefItem(APIControlHrefItemBasic):
    id: int
    tags: list[str]

    create_at: datetime.datetime
    update_at: datetime.datetime


class APIControlHrefGroupBasic(ControlHrefGroupBasic):
    control_href_items: list[APIControlHrefItemBasic] = list()


class APIControlHrefGroup(APIControlHrefGroupBasic):
    id: int

    control_href_items: list[APIControlHrefItem] = list()

    create_at: datetime.datetime
    update_at: datetime.datetime


class APIControlHrefGroupCreate(APIControlHrefGroupBasic):
    pass


class APIControlHrefItemUpdate(APIControlHrefItemBasic):
    id: int | None = None
    name: str | None = None
    control_data: str | None = None
    tags: list[str] | None = None


class APIControlHrefGroupUpdate(APIControlHrefGroupBasic):
    name: str | None = None
    tags: list[str] | None = None
    control_href_items: list[APIControlHrefItemUpdate] | None = list()


class APIControlHrefGroupMultipleUpdate(APIControlHrefGroupUpdate):
    id: int
