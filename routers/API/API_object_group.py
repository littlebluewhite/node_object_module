import redis
from sqlalchemy.orm import sessionmaker, Session
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Query

from general_operator.app.influxdb.influxdb import InfluxDB
from function.API.API_object_group import APIObjectGroupOperate
from dependencies.db_dependencies import create_get_db
import data.API.API_object_group as ObjectGroupSchemas
from fastapi.encoders import jsonable_encoder
from general_operator.function.create_data_structure import create_update_dict


class APIObjectGroupRouter(APIObjectGroupOperate):
    def __init__(self, module: ObjectGroupSchemas, redis_db: redis.Redis, influxdb: InfluxDB,
                 exc, db_session: sessionmaker):
        self.db_session = db_session
        self.main_schemas = module.main_schemas
        self.create_schemas = module.create_schemas
        self.update_schemas = module.update_schemas
        self.multiple_update_schemas = module.multiple_update_schemas
        self.func_plug_folder = 'object-group_client'
        APIObjectGroupOperate.__init__(self, module, redis_db, influxdb, exc)

    def create(self):
        router = APIRouter(
            prefix="/api/object_group",
            tags=["API", "Object Group"]
        )

        # In order to use type hint, add this in code
        main_schemas = self.main_schemas
        create_schemas = self.create_schemas
        update_schemas = self.update_schemas
        multiple_update_schemas = self.multiple_update_schemas

        @router.get("/", response_model=list[main_schemas])
        async def get_object_groups():
            object_group_redis_data_list: list[dict] = self.object_group_operate.read_all_data_from_redis()
            result: list = []
            for object_group in object_group_redis_data_list:
                result.append(self.format_object_group_and_objects(object_group))
            return JSONResponse(content=result)

        @router.get("/by_object_group_id", response_model=main_schemas)
        async def get_object_group_by_object_group_id(object_group_id: int = Query()):
            object_group_redis_data: list[dict] = self.object_group_operate.read_from_redis_by_key_set(
                {object_group_id})
            return JSONResponse(content=self.format_object_group_and_objects(object_group_redis_data[0]))

        @router.post("/", response_model=list[main_schemas])
        async def create_api_object_group(create_data: create_schemas,
                                          db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():

                oog_helper = create_update_dict()
                # DB table "object_group" create_data
                _mapping = self.object_group_operate.create_schemas(**create_data.dict())
                object_group = self.object_group_operate.create_data(db, data_list=[_mapping])

                if create_data.objects:

                    # No need to check here. Let sqlalchemy throw the error
                    # To examine that objects are existed in db(redis)
                    # _ = self.object_operate.read_data_from_redis_by_key_set(set(create_data.objects), 0)

                    # DB table "object_object_group" create data
                    for object_id in create_data.objects:
                        oog_helper.get("create_list").append(self.object_object_group_operate.create_schemas(
                            object_id=object_id,
                            object_group_id=object_group[0].id))
                    oog_helper["sql_list"] = self.object_object_group_operate.create_sql(db, data_list=oog_helper.get(
                        "create_list"))

                    # After creating data in sql, redis table should be updated manually
                    db.refresh(object_group[0])
                    self.object_group_operate.update_redis_table(object_group)
                    self.object_object_group_operate.update_redis_table(oog_helper["sql_list"])
                    self.object_object_group_operate.reload_redis_table(
                        db, self.object_object_group_operate.reload_related_redis_tables,
                        object_group[0], oog_helper["sql_list"])
                return JSONResponse(
                    content=[self.format_object_group_and_objects(_r) for _r in jsonable_encoder(object_group)])

        @router.post("/multiple/", response_model=list[main_schemas])
        async def create_api_object_group(create_data_list: list[create_schemas],
                                          db: Session = Depends(create_get_db(self.db_session))):
            og = create_update_dict(create=True, sql=True)
            oog = create_update_dict(create=True, sql=True)
            with db.begin():
                oog_create_list = []
                # DB table "object_group" create_data
                for create_data in create_data_list:
                    og["create_list"].append(self.object_group_operate.create_schemas(**create_data.dict()))
                og["sql_list"] = self.object_group_operate.create_data(db, data_list=og["create_list"])

                for index, create_data in enumerate(create_data_list):
                    if create_data.objects:

                        # DB table "object_object_group" create data
                        for object_id in create_data.objects:
                            oog_create_list.append(self.object_object_group_operate.create_schemas(
                                object_id=object_id,
                                object_group_id=og["sql_list"][index].id))

                oog["sql_list"] = self.object_object_group_operate.create_sql(db, data_list=oog_create_list)

                # After creating data in sql, redis table should be updated manually
                for model in og["sql_list"]:
                    db.refresh(model)
                self.object_group_operate.update_redis_table(og["sql_list"])
                self.object_object_group_operate.update_redis_table(oog["sql_list"])
                self.object_object_group_operate.reload_redis_table(
                    db, self.object_object_group_operate.reload_related_redis_tables,
                    oog["sql_list"])
                return JSONResponse(
                    content=[self.format_object_group_and_objects(_r) for _r in jsonable_encoder(og["sql_list"])])

        @router.delete("/{object_group_id}")
        async def delete_api_object_group(object_group_id: int, db: Session = Depends(create_get_db(self.db_session))):
            oog_helper = create_update_dict(create=True, sql=True, delete=True)
            with db.begin():
                # Read data first to see if oog should be deal with
                object_group_list = self.object_group_operate.read_from_redis_by_key_set({object_group_id}, 0)

                if object_group_list[0].get("objects"):
                    oog_id_list = self.object_object_group_operate.read_from_redis_by_key_set({object_group_id}, 2)
                    oog_helper["delete_data_list"] = self.object_object_group_operate.delete_sql(db,
                                                                                                 set(oog_id_list[0]))

                    self.object_object_group_operate.delete_redis_table(oog_helper["delete_data_list"])
                    self.object_object_group_operate.reload_relative_table(db, oog_helper["delete_data_list"])
                self.object_group_operate.delete_data(db, {object_group_id})
            return JSONResponse(content="Ok")

        @router.delete("/multiple/")
        async def delete_api_object_group(object_group_id_set: set[int] = Query(),
                                          db: Session = Depends(create_get_db(self.db_session))):
            oog_helper = create_update_dict(create=True, delete=True, sql=True)
            with db.begin():
                # Read object_groups' ID to get their objects included
                object_group_list: list[dict] = self.object_group_operate.read_from_redis_by_key_set(
                    object_group_id_set, 0)

                for object_group in object_group_list:
                    # If objects included in object_group, collect them in oog_helper["delete_id_set"]
                    if object_group.get("objects"):
                        _oog = self.object_object_group_operate.read_from_redis_by_key_set({object_group.get("id")}, 2)
                        oog_helper["delete_id_set"] = oog_helper["delete_id_set"].union(set(_oog[0]))

                oog_helper["delete_data_list"] = self.object_object_group_operate.delete_sql(db, oog_helper[
                    "delete_id_set"])
                del_object_group = self.object_group_operate.delete_sql(db, object_group_id_set)

                self.object_object_group_operate.delete_redis_table(oog_helper["delete_data_list"])
                self.object_group_operate.delete_redis_table(del_object_group)
                self.object_object_group_operate.reload_relative_table(db, oog_helper["delete_data_list"])
            return JSONResponse(content="Ok")

        @router.patch("/{object_group_id}", response_model=list[main_schemas])
        async def update_api_object(update_data: update_schemas, object_group_id: int,
                                    db: Session = Depends(create_get_db(self.db_session))):
            og_helper = create_update_dict(create=True, update=True, delete=True, sql=True)
            oog_helper = create_update_dict(create=True, delete=True, sql=True)
            with db.begin():
                object_group_redis_list = self.object_group_operate.read_from_redis_by_key_set({object_group_id}, 0)
                ori_object_included = [item.get("object_id") for item in object_group_redis_list[0].get("objects")]

                # Update object_group data
                og_helper["update_list"] = [
                    self.object_group_operate.multiple_update_schemas(id=object_group_id, **update_data.dict())]
                og_helper["sql_list"] = self.object_group_operate.update_sql(db, og_helper["update_list"])

                # No need to check here. Let sqlalchemy throw the error
                # Examine whether objects are existed in db(redis)
                # if update_data.objects:
                #     object = [abs(n) for n in update_data.objects]
                #     _ = self.object_operate.read_data_from_redis_by_key_set(set(object), 0)

                nn_group_data_list = []

                # If data not existed in redis, function of "read_redis_data" would raise an error
                if ori_object_included:
                    _nn_group = self.object_object_group_operate.read_from_redis_by_key_set({object_group_id}, 2)
                    nn_group_data_list: list[dict] = self.object_object_group_operate.read_from_redis_by_key_set(
                        set(_nn_group[0]), 0)

                for object_id in update_data.objects:
                    if object_id < 0 and -object_id in ori_object_included:
                        # oog_helper["delete_id_set"].add(nn_group_data.get("id"))
                        for nn_group_data in nn_group_data_list:
                            if -object_id == nn_group_data.get("object_id"):
                                oog_helper["delete_id_set"].add(nn_group_data.get("id"))
                                break
                    elif object_id > 0 and object_id in ori_object_included:
                        continue
                    elif object_id > 0 and object_id not in ori_object_included:
                        oog_helper["create_list"].append(self.object_object_group_operate.update_schemas(
                            object_id=object_id,
                            object_group_id=object_group_id))
                    else:
                        raise self.exc(status_code=404,
                                       detail=f"object_id:{-object_id} is not included in this object_group")
                oog_helper["delete_data_list"] = self.object_object_group_operate.delete_sql(db, oog_helper[
                    "delete_id_set"])
                oog_helper["sql_list"] = self.object_object_group_operate.create_sql(db, data_list=oog_helper[
                    "create_list"])
                # After creating data in sql, redis table should be updated manually
                db.refresh(og_helper["sql_list"][0])
                self.object_group_operate.update_redis_table(og_helper["sql_list"])
                self.object_object_group_operate.delete_redis_table(oog_helper["delete_data_list"])
                self.object_object_group_operate.update_redis_table(oog_helper["sql_list"])
                self.object_object_group_operate.reload_redis_table(
                    db, self.object_object_group_operate.reload_related_redis_tables,
                    oog_helper["sql_list"])

                return JSONResponse(content=[self.format_object_group_and_objects(_r) for _r in
                                             jsonable_encoder(og_helper["sql_list"])])

        @router.patch("/multiple/", response_model=list[main_schemas])
        async def update_api_object(update_data_list: list[multiple_update_schemas],
                                    db: Session = Depends(create_get_db(self.db_session))):
            og_helper = create_update_dict(create=True, update=True, delete=True, sql=True)
            oog_helper = create_update_dict(create=True, update=True, delete=True, sql=True)
            with db.begin():
                og_id_list = []
                og_objects_set = set()
                for update_data in update_data_list:
                    # To collect all objects
                    if update_data.objects:
                        og_objects_set = og_objects_set.union({abs(n) for n in update_data.objects})

                    # To collect all object_group id
                    og_id_list.append(update_data.id)

                    # To put data into schemas
                    og_helper["update_list"].append(
                        self.object_group_operate.multiple_update_schemas(**update_data.dict()))

                # No need to check here. Let sqlalchemy throw the error
                # Examine whether objects are existed in db(redis)
                # _ = self.object_operate.read_data_from_redis_by_key_set(og_objects_set, 0)

                # Mappiog original object_group and its objects
                ori_og_and_object = {}
                object_group_redis_list = self.object_group_operate.read_from_redis_by_key_set(set(og_id_list), 0)
                for object_group_redis in object_group_redis_list:
                    ori_og_and_object[object_group_redis.get("id")] = [n.get("object_id") for n in
                                                                       object_group_redis.get("objects")]

                for update_data in update_data_list:
                    for n in update_data.objects:
                        if n < 0 and -n in ori_og_and_object.get(update_data.id):
                            _oog_list = self.object_object_group_operate.read_from_redis_by_key_set({update_data.id}, 2)
                            oog_list = self.object_object_group_operate.read_from_redis_by_key_set(set(_oog_list[0]), 0)
                            for oog in oog_list:
                                if oog.get("object_id") == -n:
                                    oog_helper["delete_id_set"].add(oog.get("id"))
                                    break
                        elif n > 0 and n not in ori_og_and_object.get(update_data.id):
                            oog_helper["create_list"].append(
                                self.object_object_group_operate.update_schemas(
                                    object_id=n,
                                    object_group_id=update_data.id))
                        elif n > 0 and n in ori_og_and_object.get(update_data.id):
                            continue
                        else:
                            raise self.exc(status_code=404,
                                           detail=f"object_id:{n} is not included in this object_group")

                # Update object_group data
                og_helper["sql_list"] = self.object_group_operate.update_sql(db, og_helper["update_list"])

                # create or delete relationship
                oog_helper["delete_data_list"] = self.object_object_group_operate.delete_sql(db, oog_helper[
                    "delete_id_set"])
                oog_helper["sql_list"] = self.object_object_group_operate.create_sql(db, oog_helper["create_list"])

                for og_model in og_helper["sql_list"]:
                    db.refresh(og_model)
                self.object_group_operate.update_redis_table(og_helper["sql_list"])
                self.object_object_group_operate.delete_redis_table(oog_helper["delete_data_list"])
                self.object_object_group_operate.update_redis_table(oog_helper["sql_list"])

                self.object_object_group_operate.reload_redis_table(
                    db, self.object_object_group_operate.reload_related_redis_tables,
                    oog_helper["sql_list"])
                self.object_object_group_operate.reload_redis_table(
                    db, self.object_object_group_operate.reload_related_redis_tables,
                    oog_helper["delete_data_list"])

                return JSONResponse(content=[self.format_object_group_and_objects(_r) for _r in
                                             jsonable_encoder(og_helper["sql_list"])])

        return router
