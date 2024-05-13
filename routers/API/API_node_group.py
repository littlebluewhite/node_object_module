import redis
from sqlalchemy.orm import sessionmaker, Session
from fastapi import APIRouter, Depends, Query, Security
from fastapi.responses import JSONResponse

from general_operator.app.influxdb.influxdb import InfluxDB
from function.API.API_node_group import APINodeGroupOperate
from dependencies.db_dependencies import create_get_db
import data.API.API_node_group as NodeGroupSchemas
from fastapi.encoders import jsonable_encoder
from general_operator.function.create_data_structure import create_update_dict


class APINodeGroupRouter(APINodeGroupOperate):
    def __init__(self, module: NodeGroupSchemas, redis_db: redis.Redis, influxdb: InfluxDB, exc, db_session: sessionmaker):
        self.db_session = db_session
        self.main_schemas = module.main_schemas
        self.create_schemas = module.create_schemas
        self.update_schemas = module.update_schemas
        self.multiple_update_schemas = module.multiple_update_schemas
        self.node_schemas = module.node_schemas
        self.func_plug_folder = 'node-group_client'
        APINodeGroupOperate.__init__(self, module, redis_db, influxdb, exc)

    def create(self, api_key_header):
        router = APIRouter(
            prefix="/api/node_group",
            tags=["API", "Node Group"]
        )
        # In order to use type hint, add this in code
        main_schemas = self.main_schemas
        create_schemas = self.create_schemas
        update_schemas = self.update_schemas
        multiple_update_schemas = self.multiple_update_schemas

        @router.get("/", response_model=list[self.main_schemas])
        async def get_node_groups(api_key=Security(api_key_header)):
            node_group_redis_data_list: list[dict] = self.node_group_operate.read_all_data_from_redis()
            result: list = []
            for node_group in node_group_redis_data_list:
                result.append(self.format_node_group_and_nodes(node_group))
            return JSONResponse(content=result)

        @router.get("/by_node_group_id", response_model=main_schemas)
        async def get_node_group_by_node_group_id(node_group_id: int = Query()):
            node_group_redis_data: list[dict] = self.node_group_operate.read_from_redis_by_key_set({node_group_id})
            return JSONResponse(content=self.format_node_group_and_nodes(node_group_redis_data[0]))

        @router.post("/", response_model=list[main_schemas])
        async def create_api_node_group(create_data: create_schemas,
                                        db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():

                nng_helper = create_update_dict()
                # DB table "node_group" create_data
                _mapping: create_schemas = self.node_group_operate.create_schemas(**create_data.dict())
                node_group = self.node_group_operate.create_data(db, data_list=[_mapping])

                if create_data.nodes:

                    # No need to check here. Let sqlalchemy throw the error
                    # Action here to examine that nodes are existed in db(redis)
                    # _ = self.node_operate.read_data_from_redis_by_key_set(set(create_data.nodes), 0)

                    # DB table "node_node_group" create data
                    for node_id in create_data.nodes:
                        nng_helper.get("create_list").append(self.node_node_group_operate.create_schemas(
                            node_id=node_id,
                            node_group_id=node_group[0].id))
                    nng_helper["sql_list"] = self.node_node_group_operate.create_sql(db, data_list=nng_helper.get(
                        "create_list"))

                    # After creating data in sql, redis table should be updated manually
                    db.refresh(node_group[0])
                    self.node_group_operate.update_redis_table(node_group)
                    self.node_node_group_operate.update_redis_table(nng_helper["sql_list"])
                    self.node_node_group_operate.reload_redis_table(db,
                                                                    self.node_node_group_operate.reload_related_redis_tables,
                                                                    nng_helper["sql_list"])

                return JSONResponse(
                    content=[self.format_node_group_and_nodes(_r) for _r in jsonable_encoder(node_group)])

        @router.post("/multiple/", response_model=list[main_schemas])
        async def create_api_node_group(create_data_list: list[create_schemas],
                                        db: Session = Depends(create_get_db(self.db_session))):
            ng = create_update_dict(create=True, sql=True)
            nng = create_update_dict(create=True, sql=True)
            with db.begin():
                nng_create_list = []
                # DB table "node_group" create_data
                for create_data in create_data_list:
                    ng["create_list"].append(self.node_group_operate.create_schemas(**create_data.dict()))
                ng["sql_list"] = self.node_group_operate.create_data(db, data_list=ng["create_list"])

                for index, create_data in enumerate(create_data_list):
                    if create_data.nodes:

                        # No need to check here. Let sqlalchemy throw the error
                        # To examine that nodes are existed in db(redis)
                        # _ = self.node_operate.read_data_from_redis_by_key_set(set(create_data.nodes), 0)

                        # DB table "node_node_group" create data
                        for node_id in create_data.nodes:
                            nng_create_list.append(self.node_node_group_operate.create_schemas(
                                node_id=node_id,
                                node_group_id=ng["sql_list"][index].id))

                nng["sql_list"] = self.node_node_group_operate.create_sql(db, data_list=nng_create_list)

                # After creating data in sql, redis table should be updated manually
                for model in ng["sql_list"]:
                    db.refresh(model)
                self.node_group_operate.update_redis_table(ng["sql_list"])
                self.node_node_group_operate.update_redis_table(nng["sql_list"])
                self.node_node_group_operate.reload_redis_table(db,
                                                                self.node_node_group_operate.reload_related_redis_tables,
                                                                nng["sql_list"])
                return JSONResponse(
                    content=[self.format_node_group_and_nodes(_r) for _r in jsonable_encoder(ng["sql_list"])])

        @router.delete("/{node_group_id}")
        async def delete_api_node_group(node_group_id: int, db: Session = Depends(create_get_db(self.db_session))):
            nng_helper = create_update_dict(create=True, sql=True, delete=True)
            with db.begin():

                # # Read data first to see if nng should be deal with
                node_group_list = self.node_group_operate.read_from_redis_by_key_set({node_group_id}, 0)

                if node_group_list[0].get("nodes"):
                    nng_id_list = self.node_node_group_operate.read_from_redis_by_key_set({node_group_id}, 2)
                    nng_helper["delete_data_list"] = self.node_node_group_operate.delete_sql(db, set(nng_id_list[0]))

                    self.node_node_group_operate.delete_redis_table(nng_helper["delete_data_list"])
                    self.node_node_group_operate.reload_relative_table(db, nng_helper["delete_data_list"])
                self.node_group_operate.delete_data(db, {node_group_id})
            return JSONResponse(content="Ok")

        @router.delete("/multiple/")
        async def delete_api_node_group(node_group_id_set: set[int] = Query(...),
                                        db: Session = Depends(create_get_db(self.db_session))):
            nng_helper = create_update_dict(create=True, delete=True, sql=True)
            with db.begin():
                # Read node_groups' ID to get their nodes included
                node_group_list: list[dict] = self.node_group_operate.read_from_redis_by_key_set(node_group_id_set, 0)

                for node_group in node_group_list:
                    # If nodes included in node_group, collect them in nng_helper["delete_id_set"]
                    if node_group.get("nodes"):
                        _nng = self.node_node_group_operate.read_from_redis_by_key_set({node_group.get("id")}, 2)
                        nng_helper["delete_id_set"] = nng_helper["delete_id_set"].union(set(_nng[0]))

                nng_helper["delete_data_list"] = self.node_node_group_operate.delete_sql(db,
                                                                                         nng_helper["delete_id_set"])
                del_node_group = self.node_group_operate.delete_sql(db, node_group_id_set)

                self.node_node_group_operate.delete_redis_table(nng_helper["delete_data_list"])
                self.node_group_operate.delete_redis_table(del_node_group)
                self.node_node_group_operate.reload_relative_table(db, nng_helper["delete_data_list"])
            return JSONResponse(content="Ok")

        @router.patch("/{node_group_id}", response_model=list[main_schemas])
        async def update_api_node(update_data: update_schemas, node_group_id: int,
                                  db: Session = Depends(create_get_db(self.db_session))):
            ng_helper = create_update_dict(create=True, update=True, delete=True, sql=True)
            nng_helper = create_update_dict(create=True, delete=True, sql=True)
            with db.begin():
                node_group_redis_list = self.node_group_operate.read_from_redis_by_key_set({node_group_id}, 0)
                ori_node_included = [item.get("node_id") for item in node_group_redis_list[0].get("nodes")]

                # Update node_group data
                ng_helper["update_list"] = [multiple_update_schemas(id=node_group_id, **update_data.dict())]
                ng_helper["sql_list"] = self.node_group_operate.update_sql(db, ng_helper["update_list"])

                # No need to check here. Let sqlalchemy throw the error
                # Examine whether nodes are existed in db(redis)
                # if update_data.nodes:
                #     node = [abs(n) for n in update_data.nodes]
                #     _ = self.node_operate.read_data_from_redis_by_key_set(set(node), 0)

                nn_group_data_list = []

                # If data not existed in redis, function of "read_redis_data" would raise an error
                if ori_node_included:
                    _nn_group = self.node_node_group_operate.read_from_redis_by_key_set({node_group_id}, 2)
                    nn_group_data_list: list[dict] = self.node_node_group_operate.read_from_redis_by_key_set(
                        set(_nn_group[0]), 0)

                for node_id in update_data.nodes:
                    if node_id < 0 and -node_id in ori_node_included:
                        flag = False
                        # nng_helper["delete_id_set"].add(nn_group_data.get("id"))
                        for nn_group_data in nn_group_data_list:
                            if -node_id == nn_group_data.get("node_id"):
                                nng_helper["delete_id_set"].add(nn_group_data.get("id"))
                                flag = True
                                break
                        # if not flag:
                        #     raise self.exc(status_code=404, detail=f"node_id:{-node_id} is not included in this node_group")
                    elif node_id > 0 and node_id in ori_node_included:
                        continue
                    elif node_id > 0 and node_id not in ori_node_included:
                        nng_helper["create_list"].append(self.node_node_group_operate.update_schemas(
                            node_id=node_id,
                            node_group_id=node_group_id))
                    else:
                        raise self.exc(status_code=404, detail=f"node_id:{-node_id} is not included in this node_group")
                nng_helper["delete_data_list"] = self.node_node_group_operate.delete_sql(db,
                                                                                         nng_helper["delete_id_set"])
                nng_helper["sql_list"] = self.node_node_group_operate.create_sql(db,
                                                                                 data_list=nng_helper["create_list"])
                # After creating data in sql, redis table should be updated manually
                db.refresh(ng_helper["sql_list"][0])
                self.node_group_operate.update_redis_table(ng_helper["sql_list"])
                self.node_node_group_operate.delete_redis_table(nng_helper["delete_data_list"])
                self.node_node_group_operate.update_redis_table(nng_helper["sql_list"])
                self.node_node_group_operate.reload_redis_table(db,
                                                                self.node_node_group_operate.reload_related_redis_tables,
                                                                nng_helper["sql_list"])
                return JSONResponse(
                    content=[self.format_node_group_and_nodes(_r) for _r in jsonable_encoder(ng_helper["sql_list"])])

        @router.patch("/multiple/", response_model=list[main_schemas])
        async def update_api_node(update_data_list: list[multiple_update_schemas],
                                  db: Session = Depends(create_get_db(self.db_session))):
            ng_helper = create_update_dict(create=True, update=True, delete=True, sql=True)
            nng_helper = create_update_dict(create=True, update=True, delete=True, sql=True)
            with db.begin():
                ng_id_list = []
                ng_nodes_set = set()
                for update_data in update_data_list:
                    # To collect all nodes
                    if update_data.nodes:
                        ng_nodes_set = ng_nodes_set.union({abs(n) for n in update_data.nodes})

                    # To collect all node_group id
                    ng_id_list.append(update_data.id)

                    # To put data into schemas
                    ng_helper["update_list"].append(
                        self.node_group_operate.multiple_update_schemas(**update_data.dict()))

                # No need to check here. Let sqlalchemy throw the error
                # Examine whether nodes are existed in db(redis)
                # _ = self.node_operate.read_data_from_redis_by_key_set(ng_nodes_set, 0)

                # Mapping original node_group and its nodes
                ori_ng_and_node = {}
                node_group_redis_list = self.node_group_operate.read_from_redis_by_key_set(set(ng_id_list), 0)
                for node_group_redis in node_group_redis_list:
                    ori_ng_and_node[node_group_redis.get("id")] = [n.get("node_id") for n in
                                                                   node_group_redis.get("nodes")]

                for update_data in update_data_list:
                    for n in update_data.nodes:
                        if n < 0 and -n in ori_ng_and_node.get(update_data.id):
                            _nng_list = self.node_node_group_operate.read_from_redis_by_key_set({update_data.id}, 2)
                            nng_list = self.node_node_group_operate.read_from_redis_by_key_set(set(_nng_list[0]), 0)
                            for nng in nng_list:
                                if nng.get("node_id") == -n:
                                    nng_helper["delete_id_set"].add(nng.get("id"))
                                    break
                        elif n > 0 and n not in ori_ng_and_node.get(update_data.id):
                            nng_helper["create_list"].append(
                                self.node_node_group_operate.update_schemas(
                                    node_id=n,
                                    node_group_id=update_data.id))
                        elif n > 0 and n in ori_ng_and_node.get(update_data.id):
                            continue
                        else:
                            raise self.exc(status_code=404, detail=f"node_id:{n} is not included in this node_group")

                # Update node_group data
                ng_helper["sql_list"] = self.node_group_operate.update_sql(db, ng_helper["update_list"])

                # create or delete relationship
                nng_helper["delete_data_list"] = self.node_node_group_operate.delete_sql(db,
                                                                                         nng_helper["delete_id_set"])
                nng_helper["sql_list"] = self.node_node_group_operate.create_sql(db, nng_helper["create_list"])

                for ng_model in ng_helper["sql_list"]:
                    db.refresh(ng_model)
                self.node_group_operate.update_redis_table(ng_helper["sql_list"])
                self.node_node_group_operate.delete_redis_table(nng_helper["delete_data_list"])
                self.node_node_group_operate.update_redis_table(nng_helper["sql_list"])

                self.node_node_group_operate.reload_redis_table(db,
                                                                self.node_node_group_operate.reload_related_redis_tables,
                                                                nng_helper["sql_list"])
                self.node_node_group_operate.reload_redis_table(db,
                                                                self.node_node_group_operate.reload_related_redis_tables,
                                                                nng_helper["delete_data_list"])

                return JSONResponse(
                    content=[self.format_node_group_and_nodes(_r) for _r in jsonable_encoder(ng_helper["sql_list"])])

        @router.get("/get_nodes", response_model=list[self.node_schemas])
        async def get_all_nodes_by_node_group_id(node_group_id: int = Query()):
            node_group_redis_data: list[dict] = self.node_group_operate.read_from_redis_by_key_set({node_group_id})
            group_node = {_dict.get("node_id") for _dict in node_group_redis_data[0].get("nodes")}
            to_search = group_node.copy()
            while to_search:
                node_list = self.node_operate.read_from_redis_by_key_set(to_search)
                for node in node_list:
                    to_search.update({_node.get("id") for _node in node.get("child_nodes")})
                    to_search.difference_update(group_node)
                    group_node.update(to_search)
            nodes = self.node_operate.read_from_redis_by_key_set(group_node)
            return JSONResponse(content=[self.format_api_node(i) for i in nodes])

        return router
