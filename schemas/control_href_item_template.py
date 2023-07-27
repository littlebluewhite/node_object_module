import datetime

from pydantic import BaseModel


class ControlHrefItemTemplateBasic(BaseModel):
    name: str
    control_data: str
    color: str | None = None
    control_href_group_template_id: int | None = None


class ControlHrefItemTemplate(ControlHrefItemTemplateBasic):
    id: int

    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class ControlHrefItemTemplateCreate(ControlHrefItemTemplateBasic):
    pass


class ControlHrefItemTemplateUpdate(ControlHrefItemTemplateBasic):
    name: str | None = None
    control_data: str | None = None


class ControlHrefItemTemplateMultipleUpdate(ControlHrefItemTemplateUpdate):
    id: int
