import datetime

from pydantic import BaseModel

import node_object_schemes.object_base
import node_object_schemes.fake_data_config
import node_object_schemes.control_href_group


class ObjectObjectGroup(BaseModel):
    object_group_id: int

    class Config:
        orm_mode = True


class ObjectBasic(BaseModel):
    name: str
    object_id: str
    object_base_id: int | None = None
    node_id: int | None = None
    control_href_group_id: int | None = None
    tags: list[str] = list()


class Object(ObjectBasic):
    id: str
    tags: list[str]

    create_at: datetime.datetime
    update_at: datetime.datetime

    object_base: node_object_schemes.object_base.ObjectBase | None = None
    fake_data_config: node_object_schemes.fake_data_config.FakeDataConfig | None = None
    control_href_group: node_object_schemes.control_href_group.ControlHrefGroup | None = None
    object_groups: list[ObjectObjectGroup] = list()

    class Config:
        orm_mode = True


class ObjectCreate(ObjectBasic):
    pass


class ObjectUpdate(ObjectBasic):
    object_id: str | None = None
    name: str | None = None
    tags: list[str] | None = None


class ObjectMultipleUpdate(ObjectUpdate):
    id: int
