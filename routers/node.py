from fastapi import APIRouter

from node_object_data import node_data
from node_object_function.general_operate import GeneralOperate

router = APIRouter(
    prefix="/dispatch_reply",
    tags=["reply", "Table CRUD API"],
    dependencies=[]
)

node_operate = GeneralOperate(node_data)