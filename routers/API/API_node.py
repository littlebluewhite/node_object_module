import redis

from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker, Session

from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.dependencies.get_query_dependencies import CommonQuery, SimpleQuery
from dependencies.db_dependencies import create_get_db
from function.API.API_node import APINodeOperate
import data.API.API_node as NodeSchemas


class APINodeRouter(APINodeOperate):
    def __init__(self, module: NodeSchemas, redis_db: redis.Redis, influxdb: InfluxDB, exc, db_session: sessionmaker):
        self.db_session = db_session
        self.simple_schemas = module.simple_schemas
        self.main_schemas = module.main_schemas
        self.update_schemas = module.update_schemas
        APINodeOperate.__init__(self, module, redis_db, influxdb, exc)

    def create(self):
        router = APIRouter(
            prefix="/api/node",
            tags=["API", "Node"],
            dependencies=[]
        )
        main_schemas = self.main_schemas
        create_schemas = self.create_schemas
        update_schemas = self.update_schemas
        multiple_update_schemas = self.multiple_update_schemas

        @router.get("/", response_model=list[main_schemas])
        async def get_nodes(common: CommonQuery = Depends(),
                            db: Session = Depends(create_get_db(self.db_session))):
            if common.pattern == "all":
                nodes = self.node_operate.read_all_data_from_redis()[common.skip:][:common.limit]
            else:
                id_set = self.node_operate.execute_sql_where_command(db, common.where_command)
                nodes = self.node_operate.read_from_redis_by_key_set(id_set)[common.skip:][:common.limit]
            return JSONResponse(content=[self.format_api_node(i) for i in nodes])

        @router.get("/simple/", response_model=list[self.simple_schemas])
        async def get_simple_nodes(common: SimpleQuery = Depends()):
            nodes = self.node_operate.read_all_data_from_redis()[common.skip:][:common.limit]
            return JSONResponse(content=[self.format_simple_api_node(node) for node in nodes])

        @router.get("/by_uid/", response_model=list[main_schemas])
        async def get_nodes_by_node_id(common: CommonQuery = Depends(),
                                       key: str = Query(...),
                                       db: Session = Depends(create_get_db(self.db_session))):
            key_set = set(key.replace(" ", "").split(","))
            id_list = self.node_operate.read_from_redis_by_key_set(key_set, 1)
            id_set = {i[0] for i in id_list}
            if common.pattern == "search":
                id_set1 = self.node_operate.execute_sql_where_command(db, common.where_command)
                id_set = id_set | id_set1
            nodes = self.node_operate.read_from_redis_by_key_set(id_set)[common.skip:][:common.limit]
            return JSONResponse(content=[self.format_api_node(i) for i in nodes])

        @router.post("/", response_model=main_schemas)
        async def create_api_node(create_data: create_schemas,
                                  db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                create_dict = create_data.dict()
                # DB table "node_base" create data
                node_base_create = self.node_base_operate.create_schemas(**create_dict["node_base"])
                node_base = self.node_base_operate.create_sql(db, [node_base_create])[0]
                # DB table "node" create data
                node_create = self.node_operate.create_schemas(**create_dict, node_base_id=node_base.id)
                node = self.node_operate.create_sql(db, [node_create])[0]
                # if "device info" exists, DB table "device_info" create data
                if create_dict["node_base"]["device_info"]:
                    device_info_create = self.device_info_operate.create_schemas(
                        **create_dict["node_base"]["device_info"], node_base_id=node_base.id)
                    device_info_list = self.device_info_operate.create_sql(db, [device_info_create])
                # if "third_dimension_instance" exists, DB table "third_dimension_instance" create data
                if create_dict["third_dimension_instance"]:
                    third_dimension_instance_create = self.third_d_operate.create_schemas(
                        **create_dict["third_dimension_instance"], node_id=node.id)
                    third_dimension_instance_list = self.third_d_operate.create_sql(
                        db, [third_dimension_instance_create])
                # if "node_groups" exists, DB table "node_group" create data
                if create_dict["node_groups"]:
                    _nng_schemas = [self.nn_group_operate.create_schemas(
                        node_id=node.id,
                        node_group_id=ng_id
                    ) for ng_id in create_dict["node_groups"]]
                    nn_group_instance_list = self.nn_group_operate.create_sql(db, _nng_schemas)
                db.refresh(node_base)
                db.refresh(node)

                # redis_db create data
                if create_dict["node_base"]["device_info"]:
                    self.device_info_operate.update_redis_table(device_info_list)
                if create_dict["third_dimension_instance"]:
                    self.third_d_operate.update_redis_table(third_dimension_instance_list)
                if create_dict["node_groups"]:
                    self.nn_group_operate.update_redis_table(nn_group_instance_list)
                self.node_base_operate.update_redis_table([node_base])
                self.node_operate.update_redis_table([node])

                # redis_db reload table --> parent node
                self.node_operate.reload_redis_table(db, self.node_operate.reload_related_redis_tables, [node])
                if create_dict["node_groups"]:
                    node_group_instance_list = self.node_group_operate.read_data_from_sql_by_id_set(db, set(
                        create_dict["node_groups"]))
                    self.node_group_operate.update_redis_table(node_group_instance_list)

                return JSONResponse(content=self.format_api_node(jsonable_encoder(node)))

        @router.post("/multiple/", response_model=list[main_schemas])
        async def create_api_nodes(create_data_list: list[create_schemas],
                                   db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                create_dict_list = []
                node_base_create_list = []
                device_info_dict_list = []
                tdi_dict_list = []
                _nng_schemas = []
                for create_data in create_data_list:
                    create_dict = create_data.dict()
                    create_dict_list.append(create_dict)
                    if create_dict["node_base"]["device_info"]:
                        device_info_dict_list.append(create_dict["node_base"]["device_info"])
                    else:
                        device_info_dict_list.append(None)
                    if create_dict["third_dimension_instance"]:
                        tdi_dict_list.append(create_dict["third_dimension_instance"])
                    else:
                        tdi_dict_list.append(None)
                    node_base_create_list.append(self.node_base_operate.create_schemas(**create_dict["node_base"]))

                node_base_list = self.node_base_operate.create_sql(db, node_base_create_list)
                node_create_list = []
                for create_dict, node_base in zip(create_dict_list, node_base_list):
                    node_create = self.node_operate.create_schemas(**create_dict, node_base_id=node_base.id)
                    node_create_list.append(node_create)
                node_list = self.node_operate.create_sql(db, node_create_list)

                uid_id_mapping = {node.uid: node.id for node in node_list}

                for create_data in create_data_list:
                    create_dict = create_data.dict()
                    if create_dict["node_groups"]:
                        _nng_schemas.extend([self.nn_group_operate.create_schemas(
                            node_id=uid_id_mapping[create_dict["uid"]],
                            node_group_id=ng_id
                        ) for ng_id in create_dict["node_groups"]])
                if _nng_schemas:
                    nn_group_instance_list = self.nn_group_operate.create_sql(db, _nng_schemas)
                    ng_affected_set = set([nng.node_group_id for nng in nn_group_instance_list])

                device_info_create_list = []
                for node_base, device_info_dict in zip(node_base_list, device_info_dict_list):
                    if device_info_dict is None:
                        continue
                    else:
                        device_info_create = self.device_info_operate.create_schemas(
                            **device_info_dict, node_base_id=node_base.id)
                        device_info_create_list.append(device_info_create)
                device_info_list = self.device_info_operate.create_sql(db, device_info_create_list)
                tdi_create_list = []
                for node, tdi_dict in zip(node_list, tdi_dict_list):
                    if tdi_dict is None:
                        continue
                    else:
                        tdi_create_list.append(self.third_d_operate.create_schemas(**tdi_dict, node_id=node.id))
                tdi_list = self.third_d_operate.create_sql(db, tdi_create_list)

                for node_base in node_base_list:
                    db.refresh(node_base)
                for node in node_list:
                    db.refresh(node)
                if device_info_list:
                    self.device_info_operate.update_redis_table(device_info_list)
                if tdi_list:
                    self.third_d_operate.update_redis_table(tdi_list)
                self.node_base_operate.update_redis_table(node_base_list)
                self.node_operate.update_redis_table(node_list)

                if _nng_schemas:
                    node_group_instance_list = self.node_group_operate.read_data_from_sql_by_id_set(db, ng_affected_set)
                    self.node_group_operate.update_redis_table(node_group_instance_list)
                    self.nn_group_operate.update_redis_table(nn_group_instance_list)
                    self.nn_group_operate.reload_redis_table(db, self.nn_group_operate.reload_related_redis_tables,
                                                             nn_group_instance_list)

                self.node_operate.reload_redis_table(db, self.node_operate.reload_related_redis_tables, node_list)

                return JSONResponse(content=[self.format_api_node(node) for node in jsonable_encoder(node_list)])

        @router.patch("/{_id}", response_model=main_schemas)
        async def update_api_node(update_data: update_schemas, _id: int,
                                  db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                node_list = self.update_multiple_node([multiple_update_schemas(id=_id, **update_data.dict())], db)
                return JSONResponse(content=self.format_api_node(jsonable_encoder(node_list[0])))

        @router.patch("/multiple/", response_model=list[main_schemas])
        async def update_api_nodes(
                update_list: list[multiple_update_schemas],
                db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                node = self.update_multiple_node(update_list, db)
                return JSONResponse(content=[self.format_api_node(i) for i in jsonable_encoder(node)])

        @router.delete("/{node_id}")
        async def delete_api_node(node_id: int, db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                return JSONResponse(content=self.delete_nodes_including_object(db, {node_id}))

        @router.delete("/without_affecting_object/{node_id}")
        async def delete_api_node(_id: int, db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                return JSONResponse(content=self.delete_nodes_excluding_object(db, {_id}))

        @router.delete("/multiple/")
        async def delete_api_nodes(id_set: set[int] = Query(...),
                                   db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                return JSONResponse(content=self.delete_nodes_including_object(db, id_set))

        @router.delete("/multiple/without_affecting_object")
        async def delete_api_nodes(id_set: set[int] = Query(...),
                                   db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                return JSONResponse(content=self.delete_nodes_excluding_object(db, id_set))

        return router
