from schemas.node_group import NodeGroupBasic
import datetime


class APINodeGroupMain(NodeGroupBasic):
    id: int
    updated_at: datetime.datetime
    nodes: list[int]

class APINodeGroupCreate(NodeGroupBasic):
    nodes: list[int]

class APINodeGroupUpdate(NodeGroupBasic):
    uid: str | None = None
    nodes: list[int]
    
class APINodeGroupMultipleUpdate(APINodeGroupUpdate):
    id: int