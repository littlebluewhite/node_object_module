import datetime

from pydantic import BaseModel
from schemas.control_href_group import ControlHrefGroupBasic


class APIControlHrefItemBasic(BaseModel):
    name: str | None = None
    control_data: str | None = None
    color: str | None = None
    tags: list[str] = list()


class APIControlHrefGroupSimple(BaseModel):
    id: int
    uid: str | None


class APIControlHrefItem(APIControlHrefItemBasic):
    id: int
    tags: list[str]

    created_at: datetime.datetime
    updated_at: datetime.datetime


class APIControlHrefGroupBasic(ControlHrefGroupBasic):
    control_href_items: list[APIControlHrefItemBasic] = list()


class APIControlHrefGroup(APIControlHrefGroupBasic):
    id: int

    control_href_items: list[APIControlHrefItem] = list()

    created_at: datetime.datetime
    updated_at: datetime.datetime


class APIControlHrefGroupCreate(APIControlHrefGroupBasic):
    pass


class APIControlHrefItemUpdate(APIControlHrefItemBasic):
    id: int | None = None
    name: str | None = None
    control_data: str | None = None
    tags: list[str] | None = None


class APIControlHrefGroupUpdate(APIControlHrefGroupBasic):
    uid: str | None = None
    tags: list[str] | None = None
    control_href_items: list[APIControlHrefItemUpdate] | None = list()


class APIControlHrefGroupMultipleUpdate(APIControlHrefGroupUpdate):
    id: int
