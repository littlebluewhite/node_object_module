import datetime

from pydantic import BaseModel

import schemas.object_base
import schemas.fake_data_config


class ObjectObjectGroup(BaseModel):
    object_group_id: int

    class Config:
        orm_mode = True


class ObjectBasic(BaseModel):
    name: str
    uid: str
    source_id: str | None = None
    node_id: int | None = None
    control_href_group_id: int | None = None
    tags: list[str] = list()


class Object(ObjectBasic):
    id: int
    tags: list[str]

    object_base_id: int | None = None

    created_at: datetime.datetime
    updated_at: datetime.datetime

    object_base: schemas.object_base.ObjectBase | None = None
    fake_data_config: schemas.fake_data_config.FakeDataConfig | None = None
    object_groups: list[ObjectObjectGroup] = list()

    class Config:
        orm_mode = True


class ObjectCreate(ObjectBasic):
    object_base_id: int | None = None


class ObjectUpdate(ObjectBasic):
    uid: str | None = None
    source_id: str | None = None
    name: str | None = None
    tags: list[str] | None = None
    node_id: int | str | None = None
    object_base_id: int | None = None
    control_href_group_id: int | str | None = None


class ObjectMultipleUpdate(ObjectUpdate):
    id: int
