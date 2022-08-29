from typing import Optional
from pydantic import BaseModel


class ControlHrefItemBase(BaseModel):
    name: str  # 控制選項名稱
    control_data: str  # 控制選項所要送出的DATA或URL
    color: str  # 控制選項的顏色，以色票的方式


class ControlHrefItem(ControlHrefItemBase):
    id: int

    class Config:
        orm_mode = True


class ControlHrefItemUpdate(ControlHrefItemBase): ...


class ControlHrefItemUpdateById(ControlHrefItemBase):
    id: int


class ControlHrefItemDeleteById(ControlHrefItemUpdateById): ...
