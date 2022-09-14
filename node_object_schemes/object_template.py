import datetime

from pydantic import BaseModel

import node_object_schemes.object_base
import node_object_schemes.control_href_group_template
import node_object_schemes.fake_data_config_template


class ObjectTemplateBasic(BaseModel):
    name: str
    object_base_id: int | None = None
    node_template_id: int | None = None


class ObjectTemplate(ObjectTemplateBasic):
    id: int

    update_at: datetime.datetime

    object_base: node_object_schemes.object_base.ObjectBase | None = None
    control_href_group_template: node_object_schemes.control_href_group_template.ControlHrefGroupTemplate | None = None
    fake_data_config_template: node_object_schemes.fake_data_config_template.FakeDataConfigTemplate | None = None

    class Config:
        orm_mode = True


class ObjectTemplateCreate(ObjectTemplateBasic):
    pass


class ObjectTemplateUpdate(ObjectTemplateBasic):
    name: str | None = None


class ObjectTemplateMultipleUpdate(ObjectTemplateUpdate):
    id: int
