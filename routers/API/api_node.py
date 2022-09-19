import redis
from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import sessionmaker, Session

import node_object_data.node
import node_object_data.node_base
import node_object_data.third_dimension_instance
import node_object_data.device_info
from dependencies.common_search_dependencies import CommonQuery
from dependencies.db_dependencies import create_get_db
from node_object_function.API.API_node import APINodeFunction
from node_object_function.General_operate import GeneralOperate


class NodeAPIRouter(APINodeFunction):
    def __init__(self, module, redis_db: redis.Redis, exc, db_session: sessionmaker):
        self.main_schemas = module.main_schemas
        self.create_schemas = module.create_schemas
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

        create_schemas = self.create_schemas

        @router.get("/", response_model=list[self.main_schemas])
        async def get_nodes(common: CommonQuery = Depends(),
                            db: Session = Depends(create_get_db(self.db_session))):
            if common.pattern == "all":
                nodes = self.node_operate.read_all_data_from_redis()[common.skip:][:common.limit]
            else:
                id_set = self.node_operate.execute_sql_where_command(db, common.where_command)
                nodes = self.node_operate.read_data_from_redis_by_key_set(id_set)[common.skip:][:common.limit]
            return [self.format_api_node(i) for i in nodes]

        @router.get("/by_node_id", response_model=list[self.main_schemas])
        async def get_nodes_by_node_id(common: CommonQuery = Depends(),
                                       key: str = Query(...),
                                       db: Session = Depends(create_get_db(self.db_session))):
            key_set = set(key.replace(" ", "").split(","))
            id_list = self.node_operate.read_data_from_redis_by_key_set(key_set, 1)
            id_set = {i[0] for i in id_list}
            if common.pattern == "search":
                id_set1 = self.node_operate.execute_sql_where_command(db, common.where_command)
                id_set = id_set | id_set1
            nodes = self.node_operate.read_data_from_redis_by_key_set(id_set)[common.skip:][:common.limit]
            return [self.format_api_node(i) for i in nodes]

        @router.post("/",
                     response_model=self.main_schemas
                     )
        async def create_api_node(create_data: create_schemas,
                                  db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                create_dict = create_data.dict()
                node_base_create = self.node_base_operate.create_schemas(**create_dict["node_base"])
                node_base = self.node_base_operate.create_multiple_sql_data(
                    db, [node_base_create], self.node_base_operate.sql_model)[0]
                node_create = self.node_operate.create_schemas(**create_dict, node_base_id=node_base.id)
                print(node_create)
                node = self.node_operate.create_multiple_sql_data(db, [node_create], self.node_operate.sql_model)[0]
                if create_dict["node_base"]["device_info"]:
                    device_info_create = self.device_info_operate.create_schemas(
                        **create_dict["node_base"]["device_info"], node_base_id=node_base.id)
                    device_info_list = self.device_info_operate.create_multiple_sql_data(
                        db, [device_info_create], self.device_info_operate.sql_model)
                    for table in self.device_info_operate.redis_tables:
                        self.device_info_operate.write_sql_data_to_redis(
                            table["name"], device_info_list, self.device_info_operate.main_schemas, table["key"]
                        )
                if create_dict["third_dimension_instance"]:
                    third_dimension_instance_create = self.third_d_operate.create_schemas(
                        **create_dict["third_dimension_instance"], node_id=node.id)
                    third_dimension_instance_list = self.third_d_operate.create_multiple_sql_data(
                        db, [third_dimension_instance_create], self.third_d_operate.sql_model)
                    for table in self.third_d_operate.redis_tables:
                        self.third_d_operate.write_sql_data_to_redis(
                            table["name"], third_dimension_instance_list, self.third_d_operate.main_schemas, table["key"])
                db.refresh(node_base)
                db.refresh(node)
                for table in self.node_base_operate.redis_tables:
                    self.node_base_operate.write_sql_data_to_redis(
                        table["name"], [node_base], self.node_base_operate.main_schemas, table["key"])
                for table in self.node_operate.redis_tables:
                    self.node_operate.write_sql_data_to_redis(
                        table["name"], [node], self.node_operate.main_schemas, table["key"]
                    )
                self.node_operate.reload_redis_table(db, self.node_operate.reload_related_redis_tables, [node])

                return jsonable_encoder(node)

        return router
