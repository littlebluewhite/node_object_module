import datetime

from pydantic import BaseModel
import schemas.control_href_item_template


class ControlHrefGroupTemplateBasic(BaseModel):
    name: str
    object_template_id: int | None = None


class ControlHrefGroupTemplate(ControlHrefGroupTemplateBasic):
    id: int

    update_at: datetime.datetime

    control_href_item_template: list[schemas.control_href_item_template.ControlHrefItemTemplate] = list()

    class Config:
        orm_mode = True


class ControlHrefGroupTemplateCreate(ControlHrefGroupTemplateBasic):
    pass


class ControlHrefGroupTemplateUpdate(ControlHrefGroupTemplateBasic):
    name: str | None = None


class ControlHrefGroupTemplateMultipleUpdate(ControlHrefGroupTemplateUpdate):
    id: int
