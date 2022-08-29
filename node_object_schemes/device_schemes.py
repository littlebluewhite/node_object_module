import datetime
from typing import Optional, List
from pydantic import BaseModel


class DeviceBase(BaseModel):
    device_id: Optional[str] = None  # 對應真實設備的id，如設備廠商的設定
    device_display_name: Optional[str or None] = None  # 顯示的設備名稱
    device_group_id: Optional[List[int]] = [0]  # 對應的設備群組id，用於反向檢索
    device_info_id: Optional[int] = 0  # 對應的設備訊息id
    device_type: Optional[str] = None  # 設備的類型，如電表、三合一檢測器、攝影機...，這邊只提供一組字串作為API檢索的一項功能
    sensor_ids: Optional[List[int]] = None  # 對應的設備訊息id

    streaming_url: Optional[str] = None  # 影像串流欄位
    image_url: Optional[str] = None  # 圖片位置
    area: Optional[str] = None  # 設備描述所屬樓層、區域
    floor: Optional[str] = "0f"  # 設備描述所屬樓層、區域

    position: Optional[str] = None  # 世界座標，呈現結果如{"x": 0.0, "y": 0.0, "z": 0.0}
    rotation: Optional[str] = None  # 旋轉Euler角(0.0~360.0)度，呈現結果如{"x": 0.0, "y": 0.0, "z": 0.0}
    scale: Optional[str] = None  # 縮放大小，呈現結果如{"x": 1.0, "y": 1.0, "z": 1.0}
    model_url: Optional[str] = None  # 模型路徑

    location_path: Optional[str] = None  # 階層路徑
    layer_id: Optional[int] = 0  # 設備定義層級(Building / Floor / Room / Device / Pipe / Sensor)

    last_maintain_date: datetime.datetime = None  # 最後維護日期
    next_maintain_date: datetime.datetime = None  # 下次維護日期


class Device(DeviceBase):
    id: int

    class Config:
        orm_mode = True


class DeviceUpdate(DeviceBase): ...


class DeviceUpdateById(DeviceBase):
    id: int


class DeviceDeleteById(DeviceUpdateById):...
