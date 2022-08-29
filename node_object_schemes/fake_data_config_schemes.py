from typing import Optional, List, Any
from pydantic import BaseModel


class FakeDataConfigBase(BaseModel):
    name: str  # 假資料名稱

    faking_frequency: Optional[int] = 5  # 打假資料的頻率
    faking_default_value: Optional[float] = 0.0  # 假資料預設值
    faking_inc_limit: Optional[float] = 0.0  # 假資料上限
    faking_dec_limit: Optional[float] = 0.0  # 假資料下限
    faking_extra_info: Optional[List[Any]] = None  # 額外可能的資料


class FakeDataConfig(FakeDataConfigBase):
    id: int

    class Config:
        orm_mode = True


class FakeDataConfigUpdate(FakeDataConfigBase): ...


class FakeDataConfigUpdateById(FakeDataConfigBase):
    id: int


class FakeDataConfigDeleteById(FakeDataConfigUpdateById): ...
