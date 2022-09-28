import redis
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import sessionmaker, Session

import node_object_data.object
import node_object_data.object_base
import node_object_data.object_object_group
import node_object_data.fake_data_config
import node_object_data.fake_data_config_base
from dependencies.common_search_dependencies import CommonQuery
from dependencies.db_dependencies import create_get_db
from node_object_function.API.API_object import APIObjectFunction
from node_object_function.General_operate import GeneralOperate


class APIObjectRouter(APIObjectFunction):
    def __init__(self, module, redis_db: redis.Redis, exc, db_session: sessionmaker):
        self.main_schemas = module.main_schemas
        self.create_schemas = module.create_schemas
        self.update_schemas = module.update_schemas
        self.multiple_update_schemas = module.multiple_update_schemas
        self.db_session = db_session
        self.exc = exc
        self.object_operate = GeneralOperate(node_object_data.object, redis_db, exc)
        self.object_base_operate = GeneralOperate(node_object_data.object_base, redis_db, exc)
        self.oo_groups_operate = GeneralOperate(node_object_data.object_object_group, redis_db, exc)
        self.fdc = GeneralOperate(node_object_data.fake_data_config, redis_db, exc)
        self.fdcBase = GeneralOperate(node_object_data.fake_data_config_base, redis_db, exc)

    def create(self):
        router = APIRouter(
            prefix="/api/object",
            tags=["API", "Object"],
            dependencies=[]
        )

        create_schemas = self.create_schemas
        update_schemas = self.update_schemas
        multiple_update_schemas = self.multiple_update_schemas

        @router.get("/", response_model=list[self.main_schemas])
        async def get_object(common: CommonQuery = Depends(),
                             db: Session = Depends(create_get_db(self.db_session))):
            if common.pattern == "all":
                objects = self.object_operate.read_all_data_from_redis()[common.skip:][:common.limit]
            else:
                id_set = self.object_operate.execute_sql_where_command(db, common.where_command)
                objects = self.object_operate.read_data_from_redis_by_key_set(id_set)[common.skip:][:common.limit]
            return {self.format_api_object(i) for i in objects}

        @router.get("/by_object_id/", response_model=list[self.main_schemas])
        async def get_objects_by_object_id(common: CommonQuery = Depends(),
                                           key: str = Query(...),
                                           db: Session = Depends(create_get_db(self.db_session))):
            key_set = set(key.replace(" ", "").split(","))
            id_list = self.object_operate.read_data_from_redis_by_key_set(key_set, 1)
            id_set = {i[0] for i in id_list}
            if common.pattern == "search":
                id_set1 = self.object_operate.execute_sql_where_command(db, common.where_command)
                id_set = id_set | id_set1
            nodes = self.object_operate.read_data_from_redis_by_key_set(id_set)[common.skip:][:common.limit]
            return [self.format_api_object(i) for i in nodes]

        @router.post("/", response_model=self.main_schemas)
        async def create_api_node(create_data: create_schemas,
                                  db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                object_dict_list = []
                object_base_create_list = []




































