import redis
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import sessionmaker, Session

import node_object_data.node
import node_object_data.node_base
import node_object_data.third_dimension_instance
import node_object_data.device_info
from dependencies.common_search_dependencies import CommonQuery
from dependencies.db_dependencies import create_get_db
from node_object_function.General_operate import GeneralOperate
from node_object_schemes.API.API_node import APINode


class NodeAPIRouter:
    def __init__(self, redis_db: redis.Redis, exc, db_session: sessionmaker):
        self.db_session = db_session
        self.node_operate = GeneralOperate(node_object_data.node, redis_db, exc)
        self.node_base_operate = GeneralOperate(node_object_data.node_base, redis_db, exc)
        self.third_d_operate = GeneralOperate(node_object_data.third_dimension_instance, redis_db, exc)
        self.device_info_operate = GeneralOperate(node_object_data.device_info, redis_db, exc)

    def create(self):
        router = APIRouter(
            prefix="/api/node",
            tags=["API", "Node"],
            dependencies=[]
        )

        @router.get("/", response_model=list[APINode])
        async def get_nodes(common: CommonQuery = Depends(),
                            db: Session = Depends(create_get_db(self.db_session))):
            if common.pattern == "all":
                s = self.node_operate.read_all_data_from_redis()[common.skip:][:common.limit]
                def ss(i):
                    ll = list()
                    for item in i["child_nodes"]:
                        ll.append(item["id"])
                    i["child_nodes"] = ll
                    return i
                s = [ss(i)for i in s]
                print(s)
                return s
                # return self.node_operate.read_all_data_from_redis()[common.skip:][:common.limit]
            else:
                id_set = self.node_operate.execute_sql_where_command(db, common.where_command)
                return self.node_operate.read_data_from_redis_by_key_set(id_set)[common.skip:][:common.limit]

        @router.get("/by_node_id", response_model=list[self.node_operate.main_schemas])
        async def get_nodes_by_node_id(common: CommonQuery = Depends(),
                                       key: str = Query(...),
                                       db: Session = Depends(create_get_db(self.db_session))):
            key_set = set(key.replace(" ", "").split(","))
            id_list = self.node_operate.read_data_from_redis_by_key_set(key_set, 1)
            id_set = {i[0] for i in id_list}
            if common.pattern == "search":
                id_set1 = self.node_operate.execute_sql_where_command(db, common.where_command)
                id_set = id_set | id_set1
            return self.node_operate.read_data_from_redis_by_key_set(id_set)[common.skip:][:common.limit]

        return router
