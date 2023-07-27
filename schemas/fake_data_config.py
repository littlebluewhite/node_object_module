import datetime

from pydantic import BaseModel

import schemas.fake_data_config_base


class FakeDataConfigBasic(BaseModel):
    name: str | None = None


class FakeDataConfig(FakeDataConfigBasic):
    id: int

    fake_data_config_base_id: int | None = None
    object_id: int | None = None
    fake_data_config_base: schemas.fake_data_config_base.FakeDataConfigBase | None = None

    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class FakeDataConfigCreate(FakeDataConfigBasic):
    fake_data_config_base_id: int | None = None
    object_id: int | None = None


class FakeDataConfigUpdate(FakeDataConfigBasic):
    fake_data_config_base_id: int | None = None
    object_id: int | None = None


class FakeDataConfigMultipleUpdate(FakeDataConfigUpdate):
    id: int
