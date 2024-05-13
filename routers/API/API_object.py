import json
import time
import redis
from fastapi import APIRouter, Depends, Query, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import sessionmaker, Session

from function.API.API_object import APIObjectOperate
from general_operator.dependencies.get_query_dependencies import CommonQuery
from dependencies.db_dependencies import create_get_db
from function.API.API_object import APIObjectFunction
from general_operator.function.General_operate import GeneralOperate
from general_operator.app.influxdb.influxdb import InfluxDB
import data.API.API_object as ObjectSchemas


class APIObjectRouter(APIObjectFunction, APIObjectOperate):
    def __init__(self, module: ObjectSchemas, redis_db: redis.Redis, influxdb: InfluxDB,
                 exc, db_session: sessionmaker):
        self.db_session = db_session
        self.redis = redis_db
        self.influxdb = influxdb
        self.simple_schemas = module.simple_schemas
        APIObjectOperate.__init__(self, module, redis_db, influxdb, exc)

    def create(self):
        router = APIRouter(
            prefix="/api/object",
            tags=["API", "Object"],
        )

        create_schemas = self.create_schemas
        update_schemas = self.update_schemas
        multiple_update_schemas = self.multiple_update_schemas
        insert_schemas = self.insert_schemas
        get_value_schemas = self.get_value_schemas
        insert_schemas_modify = self.insert_schemas_modify

        @router.on_event("startup")
        async def task_startup_event():
            GeneralOperate.clean_redis_by_name(self, "object_value")

        @router.get("/", response_model=list[self.main_schemas])
        async def get_object(common: CommonQuery = Depends(),
                             db: Session = Depends(create_get_db(self.db_session))):
            if common.pattern == "all":
                objects = self.object_operate.read_all_data_from_redis()[common.skip:][:common.limit]
            else:
                id_set = self.object_operate.execute_sql_where_command(db, common.where_command)
                objects = self.object_operate.read_from_redis_by_key_set(id_set)[common.skip:][:common.limit]
            return JSONResponse(content=[self.format_api_object(i) for i in objects])

        # @router.get("/simple/", response_model=list[self.simple_schemas])
        # async def get_simple_objects(common: SimpleQuery = Depends()):
        #     objects = self.object_operate.read_all_data_from_redis()[common.skip:][:common.limit]
        #     return JSONResponse(content=[self.format_simple_api_object(obj) for obj in objects])

        @router.get("/by_uid/", response_model=list[self.main_schemas])
        async def get_objects_by_uid(common: CommonQuery = Depends(),
                                     key: str = Query(...),
                                     db: Session = Depends(create_get_db(self.db_session))):
            key_set = set(key.replace(" ", "").split(","))
            id_list = self.object_operate.read_from_redis_by_key_set(key_set, 1)
            id_set = {i[0] for i in id_list}
            if common.pattern == "search":
                id_set1 = self.object_operate.execute_sql_where_command(db, common.where_command)
                id_set = id_set | id_set1
            objects = self.object_operate.read_from_redis_by_key_set(id_set)[common.skip:][:common.limit]
            return JSONResponse(content=[self.format_api_object(i) for i in objects])

        @router.post("/", response_model=self.main_schemas)
        async def create_api_object(create_data: create_schemas,
                                    db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                create_dict = create_data.dict()
                object_base_create = self.object_base_operate.create_schemas(**create_dict["object_base"])
                object_base = self.object_base_operate.create_sql(db, [object_base_create])[0]
                o_create = self.object_operate.create_schemas(**create_dict, object_base_id=object_base.id)
                o = self.object_operate.create_sql(db, [o_create])[0]
                if create_dict.get("fake_data_config", None):
                    fdc_base_create = self.fdcBase_operate.create_schemas(
                        **create_dict["fake_data_config"]["fake_data_config_base"])
                    fdc_base = self.fdcBase_operate.create_sql(db, [fdc_base_create])[0]
                    fdc_create = self.fdc_operate.create_schemas(
                        **create_dict["fake_data_config"], fake_data_config_base_id=fdc_base.id, object_id=o.id)
                    fdc = self.fdc_operate.create_sql(db, [fdc_create])[0]
                if create_dict["object_groups"]:
                    _oog_schemas = [self.oo_group_operate.create_schemas(
                        object_id=o.id,
                        object_group_id=og_id
                    ) for og_id in create_dict["object_groups"]]
                    oo_group_instance_list = self.oo_group_operate.create_sql(db, _oog_schemas)
                db.refresh(o)

                # redis create data
                if create_dict.get("fake_data_config", None):
                    self.fdc_operate.update_redis_table([fdc])
                    self.fdcBase_operate.update_redis_table([fdc_base])
                if create_dict["object_groups"]:
                    self.oo_group_operate.update_redis_table(oo_group_instance_list)
                self.object_operate.update_redis_table([o])
                self.object_base_operate.update_redis_table([object_base])

                # redis reload table
                self.object_operate.reload_redis_table(db, self.object_operate.reload_related_redis_tables, [o])

                return JSONResponse(content=self.format_api_object(jsonable_encoder(o)))

        @router.post("/multiple/", response_model=list[self.main_schemas])
        async def create_api_objects(create_data_list: list[create_schemas],
                                     db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                create_dict_list = []
                o_create_list = []
                o_base_create_list = []
                fdc_dict_list = []
                fdc_create_list = []
                fdc_base_create_list = []
                _oog_schemas = []

                for create_data in create_data_list:
                    create_dict = create_data.dict()
                    create_dict_list.append(create_dict)
                    if create_dict["fake_data_config"]:
                        fdc_dict_list.append(create_dict["fake_data_config"])
                        fdc_base_create_list.append(self.fdcBase_operate.create_schemas(
                            **create_dict["fake_data_config"]["fake_data_config_base"]))
                    else:
                        fdc_dict_list.append(None)

                    o_base_create_list.append(self.object_base_operate.create_schemas(**create_dict["object_base"]))
                o_base_list = self.object_base_operate.create_sql(db, o_base_create_list)
                for create_dict, o_base in zip(create_dict_list, o_base_list):
                    o_create_list.append(self.object_operate.create_schemas(**create_dict, object_base_id=o_base.id))
                o_list = self.object_operate.create_sql(db, o_create_list)

                uid_id_mapping = {ob.uid: ob.id for ob in o_list}

                for create_data in create_data_list:
                    create_dict = create_data.dict()
                    if create_dict["object_groups"]:
                        _oog_schemas.extend([self.oo_group_operate.create_schemas(
                            object_id=uid_id_mapping[create_dict["uid"]],
                            object_group_id=og_id
                        ) for og_id in create_dict["object_groups"]])
                if _oog_schemas:
                    oo_group_instance_list = self.oo_group_operate.create_sql(db, _oog_schemas)
                    # og_affected_set = set([oog.object_group_id for oog in oo_group_instance_list])

                fdc_base_list = self.fdcBase_operate.create_sql(db, fdc_base_create_list)
                fdc_base_iterator = iter(fdc_base_list)
                for o, fdc_dict in zip(o_list, fdc_dict_list):
                    if fdc_dict is None:
                        continue
                    else:
                        fdc_base = next(fdc_base_iterator)
                        fdc_create_list.append(self.fdc_operate.create_schemas(
                            **fdc_dict, object_id=o.id, fake_data_config_base_id=fdc_base.id))
                fdc_list = self.fdc_operate.create_sql(db, fdc_create_list)
                # refresh object
                for o in o_list:
                    db.refresh(o)
                # update redis table
                self.fdc_operate.update_redis_table(fdc_list)
                self.fdcBase_operate.update_redis_table(fdc_base_list)

                self.object_base_operate.update_redis_table(o_base_list)
                self.object_operate.update_redis_table(o_list)

                if _oog_schemas:
                    # object_group_instance_list = self.object_group_operate.read_data_
                    # from_sql_by_id_set(db, og_affected_set)
                    # self.object_group_operate.update_redis_table(object_group_instance_list)
                    self.oo_group_operate.update_redis_table(oo_group_instance_list)
                    self.oo_group_operate.reload_redis_table(db, self.oo_group_operate.reload_related_redis_tables,
                                                             oo_group_instance_list)

                self.object_operate.reload_redis_table(db, self.object_operate.reload_related_redis_tables, o_list)

                return JSONResponse(content=[self.format_api_object(ob) for ob in jsonable_encoder(o_list)])

        @router.patch("/{object_id}", response_model=self.main_schemas)
        async def update_api_object(update_data: update_schemas, object_id: int,
                                    db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                upt_sql_list = self.update_multiple_object(
                    [multiple_update_schemas(id=object_id, **update_data.dict())], db)
                return JSONResponse(content=self.format_api_object(jsonable_encoder(upt_sql_list[0])))

        @router.patch("/multiple/", response_model=list[self.main_schemas])
        async def update_api_object(update_list: list[multiple_update_schemas],
                                    db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                upt_sql_list = self.update_multiple_object(update_list, db)
                return JSONResponse(content=[self.format_api_object(i) for i in jsonable_encoder(upt_sql_list)])

        @router.delete("/{object_id}")
        async def delete_api_object(object_id: int, db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                self.delete_multiple_object({object_id}, db)
                return JSONResponse(content="ok")

        @router.delete("/multiple/")
        async def delete_api_objects(id_set: set[int] = Query(...),
                                     db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                self.delete_multiple_object(id_set, db)
                return JSONResponse(content="ok")

        @router.put("/insert_value/")
        async def insert_value(insert_list: list[insert_schemas], background_tasks: BackgroundTasks):
            id_set = set()
            id_value_dict: dict = dict()
            insert_data: dict = dict()
            for data in insert_list:
                id_value_dict[data.id] = (data.value, data.timestamp)
                id_set.add(data.id)
            object_list = self.object_operate.read_from_redis_by_key_set(id_set)
            timestamp = time.time()
            for data in object_list:
                v = {
                    "id": data["id"],
                    "uid": data["uid"],
                    "value": id_value_dict[data["id"]][0],
                    "timestamp": timestamp if id_value_dict[data["id"]][1] is None else id_value_dict[data["id"]][1]
                }
                insert_data[data["id"]] = v

                # 背景寫入歷史資料
                background_tasks.add_task(self.write_to_history, data["id"], data["uid"], id_value_dict[data["id"]][0])

            return JSONResponse(content="ok")

        @router.put("/insert_value_by_uid/")
        async def insert_value(insert_list: list[insert_schemas_modify], background_tasks: BackgroundTasks):
            uid_set = set()
            uid_value_dict: dict = dict()
            insert_data: dict = dict()
            for data in insert_list:
                uid_value_dict[data.uid] = (data.value, data.timestamp)
                uid_set.add(data.uid)
            _obj_mapping = self.object_operate.read_from_redis_by_key_set_return_dict(uid_set, table_index=1)
            _obj_id = {_id[0] for _id in _obj_mapping.values()}
            object_list = self.object_operate.read_from_redis_by_key_set(_obj_id)
            timestamp = time.time()
            for data in object_list:
                _template = {
                    "id": data["id"],
                    "uid": data["uid"],
                    "value": uid_value_dict[data["uid"]][0],
                    "timestamp": timestamp if uid_value_dict[data["uid"]][1] is None else uid_value_dict[data["uid"]][1]
                }
                insert_data[data["id"]] = _template
                # 背景寫入歷史資料
                background_tasks.add_task(self.write_to_history, _template["id"], _template["uid"], _template["value"])

            return JSONResponse(content="ok")

        @router.get("/value/", response_model=list[get_value_schemas])
        async def get_value(id_list: list[int] = Query(...)):
            result = []
            for _id in set(id_list):
                data = self.redis.hget("object_value", str(_id))
                if data:
                    data = json.loads(data)
                    result.append(get_value_schemas(**data))
            return JSONResponse(content=jsonable_encoder(result))

        @router.get("/value_by_uid/", response_model=list[get_value_schemas])
        async def get_value(uid_list: list[str] = Query(...)):
            result = []
            for _uid in uid_list:
                _id = self.redis.hget("object_by_uid", _uid)
                if _id:
                    data = self.redis.hget("object_value", json.loads(_id)[0])
                    if data:
                        data = json.loads(data)
                        result.append(get_value_schemas(**data))
            return JSONResponse(content=jsonable_encoder(result))

        @router.get("/history_value/", response_model=list[get_value_schemas])
        async def get_history_value(
                start: str = Query(...), stop: str = Query(""), _id: str = Query(""),
                uid: str = Query(""), skip: int = Query(0), limit: int = Query(None)):
            return JSONResponse(content=self.query_history_by_id(
                start, stop, _id, uid, skip, limit))

        return router
