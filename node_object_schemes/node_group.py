import datetime

from pydantic import BaseModel

import node_object_schemes.node_base
import node_object_schemes.third_dimension_instance


class Node(BaseModel):
    id: int
    node_id: str
    name: str
    principal_name: str | None = None
    last_maintain_date: datetime.datetime | None = None
    next_maintain_date: datetime.datetime | None = None
    tags: list[str] = list()
    parent_node_id: int | None = None
    third_dimension_instance_id: int | None = None
    node_base_id: int | None = None
    create_at: datetime.datetime
    update_at: datetime.datetime

    node_base: node_object_schemes.node_base.NodeBase | None = None
    child_nodes: list = list()
    third_dimension_instance: node_object_schemes.third_dimension_instance.ThirdDimensionInstance | None = None

    class Config:
        orm_mode = True


class NodeGroupBasic(BaseModel):
    name: str
    is_topics: bool = True
    description: str


class NodeGroup(NodeGroupBasic):
    id: str
    update_at: datetime.datetime

    nodes: list[Node] = list()

    class Config:
        orm_mode = True


class NodeGroupCreate(NodeGroupBasic):
    pass


class NodeGroupUpdate(NodeGroupBasic):
    name: str | None = None
    is_topics: bool | None = None
    description: str | None = None


class NodeGroupMultipleUpdate(NodeGroupBasic):
    id: str
