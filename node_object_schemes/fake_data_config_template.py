import datetime

from pydantic import BaseModel

import node_object_schemes.fake_data_config_base


class FakeDataConfigTemplateBasic(BaseModel):
    name: str | None = None
    fake_data_config_base: int | None = None
    object_template_id: int | None = None


class FakeDataConfigTemplate(FakeDataConfigTemplateBasic):
    id: str

    fake_data_config_base: node_object_schemes.fake_data_config_base.FakeDataConfigBase | None = None

    update_at: datetime.datetime

    class Config:
        orm_mode = True


class FakeDataConfigTemplateCreate(FakeDataConfigTemplateBasic):
    pass


class FakeDataConfigTemplateUpdate(FakeDataConfigTemplateBasic):
    pass


class FakeDataConfigTemplateMultipleUpdate(FakeDataConfigTemplateUpdate):
    id: int
