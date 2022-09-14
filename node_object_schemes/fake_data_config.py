import datetime

from pydantic import BaseModel

import node_object_schemes.fake_data_config_base


class FakeDataConfigBasic(BaseModel):
    name: str | None = None
    fake_data_config_base: int | None = None
    object_id: int | None = None


class FakeDataConfig(FakeDataConfigBasic):
    id: str

    fake_data_config_base: node_object_schemes.fake_data_config_base.FakeDataConfigBase | None = None

    create_at: datetime.datetime
    update_at: datetime.datetime

    class Config:
        orm_mode = True


class FakeDataConfigCreate(FakeDataConfigBasic):
    pass


class FakeDataConfigUpdate(FakeDataConfigBasic):
    pass


class FakeDataConfigMultipleUpdate(FakeDataConfigUpdate):
    id: int
