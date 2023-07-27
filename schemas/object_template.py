import datetime

from pydantic import BaseModel

import schemas.object_base
import schemas.control_href_group_template
import schemas.fake_data_config_template


class ObjectTemplateBasic(BaseModel):
    name: str
    object_base_id: int | None = None
    node_template_id: int | None = None


class ObjectTemplate(ObjectTemplateBasic):
    id: int

    updated_at: datetime.datetime

    object_base: schemas.object_base.ObjectBase | None = None
    control_href_group_template: schemas.control_href_group_template.ControlHrefGroupTemplate | None = None
    fake_data_config_template: schemas.fake_data_config_template.FakeDataConfigTemplate | None = None

    class Config:
        orm_mode = True


class ObjectTemplateCreate(ObjectTemplateBasic):
    pass


class ObjectTemplateUpdate(ObjectTemplateBasic):
    name: str | None = None


class ObjectTemplateMultipleUpdate(ObjectTemplateUpdate):
    id: int
