from typing import Optional, List

from pydantic import BaseModel


class SensorBase(BaseModel):
    device_tables_id: Optional[List[int]] = [0]  # 所屬設備，用以反向檢索

    object_id: Optional[str] = None # 真實的點位id，如設備廠商設定的
    value: Optional[str] = "0"  # 該點位當前的值 TODO 不一定需要
    unit: Optional[str] = None  # 該點位的單位

    name: Optional[str] = None  # 顯示名稱
    data_type: Optional[str] = None  # 描述點位Value的類型，Int、String、Float、Boolean

    calculator_reader: Optional[str] = None  # 點位讀取資料，僅限數值類
    calculator_writer: Optional[str] = None  # 點位寫入資料，僅限數值類

    max_value: Optional[float] = None  # 點位最大值，僅限數值類
    min_value: Optional[float] = None  # 點位最小值，僅限數值類
    dec: Optional[int] = 0  # 顯示上允許的小數點位數

    control_able: Optional[bool] = False  # 點位是否可控
    control_href_id: Optional[int] = 0  # 點位控制選像

    fake_data_config_id: Optional[int] = 0  # 點位所屬的假資料設定Id
    device_scheme_group_id: Optional[int] = 0  # 點位所屬群組


class Sensor(SensorBase):
    id: int

    class Config:
        orm_mode = True


class SensorUpdate(SensorBase): ...


class SensorUpdateById(SensorBase):
    id: int


class SensorDeleteById(SensorUpdateById): ...

