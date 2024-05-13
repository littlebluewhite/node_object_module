import datetime

from pydantic import BaseModel


class ObjectObjectGroup(BaseModel):
    object_id: int

    class Config:
        orm_mode = True


class ObjectGroupBasic(BaseModel):
    uid: str
    is_topic: bool = True
    description: str | None = None


class ObjectGroup(ObjectGroupBasic):
    id: int
    is_topic: bool

    objects: list[ObjectObjectGroup] = list()

    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class ObjectGroupCreate(ObjectGroupBasic):
    pass


class ObjectGroupUpdate(ObjectGroupBasic):
    uid: str | None = None
    is_topic: bool | None = None


class ObjectGroupMultipleUpdate(ObjectGroupUpdate):
    id: int
