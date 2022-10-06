import datetime

from pydantic import BaseModel

import node_object_schemes.object_base
import node_object_schemes.fake_data_config


class ObjectObjectGroup(BaseModel):
    object_group_id: int

    class Config:
        orm_mode = True


class ObjectBasic(BaseModel):
    name: str
    object_id: str
    node_id: int | None = None
    control_href_group_id: int | None = None
    tags: list[str] = list()


class Object(ObjectBasic):
    id: int
    tags: list[str]

    object_base_id: int | None = None

    create_at: datetime.datetime
    update_at: datetime.datetime

    object_base: node_object_schemes.object_base.ObjectBase | None = None
    fake_data_config: node_object_schemes.fake_data_config.FakeDataConfig | None = None
    object_groups: list[ObjectObjectGroup] = list()

    class Config:
        orm_mode = True


class ObjectCreate(ObjectBasic):
    object_base_id: int | None = None


class ObjectUpdate(ObjectBasic):
    object_id: str | None = None
    name: str | None = None
    tags: list[str] | None = None
    object_base_id: int | None = None


class ObjectMultipleUpdate(ObjectUpdate):
    id: int
