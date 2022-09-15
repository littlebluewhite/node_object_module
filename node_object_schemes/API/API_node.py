import datetime

from pydantic import BaseModel

import node_object_schemes.node_base
import node_object_schemes.object
import node_object_schemes.third_dimension_instance
from node_object_schemes.node import NodeBasic


class APINode(NodeBasic):
    id: int
    tags: list[str]

    create_at: datetime.datetime
    update_at: datetime.datetime
    child_nodes: list = list()

    node_base: node_object_schemes.node_base.NodeBase | None = None

