from pydantic import BaseModel


class ObjectObjectGroupBasic(BaseModel):
    object_id: int
    object_group_id: int


class ObjectObjectGroup(ObjectObjectGroupBasic):
    class Config:
        orm_mode = True


class ObjectObjectGroupCreate(ObjectObjectGroupBasic):
    pass


class ObjectObjectGroupUpdate(ObjectObjectGroupBasic):
    object_id: int | None = None
    object_group_id: int | None = None


class ObjectObjectGroupMultipleUpdate(ObjectObjectGroupUpdate):
    pass
