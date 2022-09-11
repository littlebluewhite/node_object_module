import datetime

from pydantic import BaseModel

import node_object_schemes.third_dimension_instance
import node_object_schemes.node_base


class NodeGroup(BaseModel):
    id: str
    name: str
    is_topics: bool = True
    description: str

    update_at: datetime.datetime

    class Config:
        orm_mode = True


class NodeBasic(BaseModel):
    node_id: str
    name: str
    principal_name: str | None = None
    last_maintain_date: datetime.datetime | None = None
    next_maintain_date: datetime.datetime | None = None
    tags: list[str] = list()
    parent_node_id: int | None = None
    third_dimension_instance_id: int | None = None


class Node(NodeBasic):
    id: int

    node_base_id: int | None = None
    create_at: datetime.datetime
    update_at: datetime.datetime

    node_base: node_object_schemes.node_base.NodeBase | None = None
    child_nodes: list = list()
    third_dimension_instance: node_object_schemes.third_dimension_instance.ThirdDimensionInstance | None = None
    node_groups: list[NodeGroup] = list()

    class Config:
        orm_mode = True


class NodeCreate(NodeBasic):
    pass


class NodeUpdate(NodeBasic):
    node_id: str | None = None
    name: str | None = None
    tags: list[str] | None = None
    node_base_id: int | None = None


class NodeMultipleUpdate(NodeUpdate):
    id: int
