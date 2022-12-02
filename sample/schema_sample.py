# import datetime
#
# from pydantic import BaseModel
#
# import schemas.third_dimension_instance
# import schemas.node_base
# import schemas.object
#
#
# class NodeGroup(BaseModel):
#     id: str
#     name: str
#     is_topics: bool = True
#     description: str
#
#     update_at: datetime.datetime
#
#     class Config:
#         orm_mode = True
#
#
# class NodeBasic(BaseModel):
#     node_id: str
#     name: str
#     principal_name: str | None = None
#     last_maintain_date: datetime.datetime | None = None
#     next_maintain_date: datetime.datetime | None = None
#     tags: list[str] = list()
#     parent_node_id: int | None = None
#     node_base_id: int | None = None
#
#
# class Node(NodeBasic):
#     id: int
#     tags: list[str]
#
#     create_at: datetime.datetime
#     update_at: datetime.datetime
#
#     node_base: schemas.node_base.NodeBase | None = None
#     child_nodes: list = list()
#     third_dimension_instance: schemas.third_dimension_instance.ThirdDimensionInstance | None = None
#     node_groups: list[NodeGroup] = list()
#     objects: list[schemas.object.Object] = list()
#
#     class Config:
#         orm_mode = True
#
#
# class NodeCreate(NodeBasic):
#     pass
#
#
# class NodeUpdate(NodeBasic):
#     node_id: str | None = None
#     name: str | None = None
#     tags: list[str] | None = None
#
#
# class NodeMultipleUpdate(NodeUpdate):
#     id: int
