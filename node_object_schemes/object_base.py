from pydantic import BaseModel


class ObjectBaseBasic(BaseModel):
    object_id: str
    value: str | None = None
    unit: str | None = None
    description: str | None = None
    data_type: str | None = None
    calculator_reader: str | None = None
    calculator_writer: str | None = None
    max_value: float | None = None
    min_value: float | None = None
    dec: int = 0
    is_control: bool = False


class ObjectBase(ObjectBaseBasic):
    id: str
    dec: int
    is_control: bool

    class Config:
        orm_mode = True


class ObjectBaseCreate(ObjectBaseBasic):
    pass


class ObjectBaseUpdate(ObjectBaseBasic):
    object_id: str | None = None
    dec: int | None = None
    is_control: bool | None = None


class ObjectBaseMultipleUpdate(ObjectBaseUpdate):
    id: int
