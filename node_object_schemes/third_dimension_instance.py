import datetime

from pydantic import BaseModel


class ThirdDimensionInstanceBasic(BaseModel):
    streaming_url: str | None = None
    image_url: str | None = None
    area: str | None = None
    floor: str | None = None
    position: str | None = None
    rotation: str | None = None
    scale: str | None = None
    model_url: str | None = None
    location_path: str | None = None
    layer_id: int | None = None


class ThirdDimensionInstance(ThirdDimensionInstanceBasic):
    id: str
    node_id: int | None = None

    update_at: datetime.datetime

    class Config:
        orm_mode = True


class ThirdDimensionInstanceCreate(ThirdDimensionInstanceBasic):
    node_id: int | None = None


class ThirdDimensionInstanceUpdate(ThirdDimensionInstanceBasic):
    node_id: int | None = None


class ThirdDimensionInstanceMultipleUpdate(ThirdDimensionInstanceUpdate):
    id: int
