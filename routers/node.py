from fastapi import APIRouter

from node_object_data import node_data
from node_object_exception import NodeObjectException
from node_object_function.general_operate import GeneralOperate
from node_object_main import redis_db, db_session

router = APIRouter(
    prefix="/dispatch_reply",
    tags=["reply", "Table CRUD API"],
    dependencies=[]
)

node_operate = GeneralOperate(node_data, redis_db, NodeObjectException)


@router.on_event("startup")
async def task_startup_event():
    node_operate.initial_redis_data(db_session)

