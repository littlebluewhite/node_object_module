import datetime

from pydantic import BaseModel


class NodeBasic(BaseModel):
    pass


class Node(NodeBasic):
    id: int
    node_id: str
    name: str
    principal_name: str | None = None
    last_maintain_date: datetime.datetime | None = None
    next_maintain_date: datetime.datetime | None = None
    tags: set[str] = set()
    parent_node_id: int | None = None
    node_base_id: int
    third_dimension_instance_id: int | None = None

    create_at: datetime.datetime
    update_at: datetime.datetime

    node_base: list
    child_nodes: list
    third_dimension_instance: list
    node_groups: list

    class Config:
        orm_mode = True


