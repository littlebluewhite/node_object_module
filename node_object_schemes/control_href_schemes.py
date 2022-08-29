from pydantic import BaseModel


class ControlHrefBase(BaseModel):
    name: str  # 控制表的名稱
    href_table: int = 0  # 控制表內含的控制選項


class ControlHref(ControlHrefBase):
    id: int

    class Config:
        orm_mode = True


class ControlHrefUpdate(ControlHrefBase):...


class ControlHrefUpdateById(ControlHrefBase):
    id: int


class ControlHrefDeleteById(ControlHrefUpdateById): ...
