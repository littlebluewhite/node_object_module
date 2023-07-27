import datetime

from pydantic import BaseModel

import schemas.node_base
import schemas.object_template


class NodeTemplateBasic(BaseModel):
    node_template_id: str
    parent_node_template_id: int | None = None
    node_base_id: int | None = None


class NodeTemplate(NodeTemplateBasic):
    id: int
    tags: list[str]

    updated_at: datetime.datetime

    node_base: schemas.node_base.NodeBase | None = None
    child_node_templates: list = list()
    object_templates: list[schemas.object_template.ObjectTemplate] = list()

    class Config:
        orm_mode = True


class NodeTemplateCreate(NodeTemplateBasic):
    pass


class NodeTemplateUpdate(NodeTemplateBasic):
    node_template_id: str | None = None


class NodeTemplateMultipleUpdate(NodeTemplateUpdate):
    id: int
