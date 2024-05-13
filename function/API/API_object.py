import influxdb_client
from sqlalchemy.orm import Session

import data.object
import data.object_group
import data.object_base
import data.object_object_group
import data.fake_data_config
import data.fake_data_config_base
from general_operator.function.General_operate import GeneralOperate
from general_operator.function.create_data_structure import create_update_dict, create_delete_dict
from schemas.API.API_object import APIObjectMultipleUpdate


class APIObjectFunction:
    @staticmethod
    def format_api_object(obj: dict):
        if obj.get("object_groups"):
            obj["object_groups"] = [item.get("object_group_id") for item in obj.get("object_groups")]
        else:
            obj["object_groups"] = []
        return obj

    @staticmethod
    def format_simple_api_object(obj:dict) -> dict:
        return {
            "id": obj["id"],
            "uid": obj["uid"],
            "name": obj["name"],
        }


class APIObjectOperate(GeneralOperate):
    def __init__(self, module, redis_db, influxdb, exc):
        self.exc = exc
        self.insert_schemas = module.insert_schemas
        self.insert_schemas_modify = module.insert_schemas_modify
        self.get_value_schemas = module.get_value_schemas
        GeneralOperate.__init__(self, module, redis_db, influxdb, exc)
        self.object_group_operate = GeneralOperate(data.object_group, redis_db, influxdb, exc)
        self.object_operate = GeneralOperate(data.object, redis_db, influxdb, exc)
        self.object_base_operate = GeneralOperate(data.object_base, redis_db, influxdb, exc)
        self.oo_group_operate = GeneralOperate(data.object_object_group, redis_db, influxdb, exc)
        self.fdc_operate = GeneralOperate(data.fake_data_config, redis_db, influxdb, exc)
        self.fdcBase_operate = GeneralOperate(data.fake_data_config_base, redis_db, influxdb, exc)

    def update_multiple_object(self, update_list: list[APIObjectMultipleUpdate], db: Session):
        update_dict_list = [i.dict() for i in update_list]
        fdc = create_update_dict()
        fdc_base = create_update_dict()
        o = create_update_dict(create=False)
        o_base = create_update_dict(create=False)
        oog = create_update_dict(delete=True)
        oog["delete_og_ids"] = set()
        original_data_list = self.object_operate.read_from_redis_by_key_set({i.id for i in update_list})
        original_key_id_dict: dict = {i["id"]: i for i in original_data_list}
        self_ref_id_dict = self.object_operate.get_self_ref_id(
            [self.object_operate.main_schemas(**i) for i in original_data_list])
        # deal with update data
        for data in update_dict_list:
            original_object: dict = original_key_id_dict[data["id"]]
            original_o_base: dict = original_object["object_base"]
            original_fdc = original_object["fake_data_config"]
            original_og: set ={i["object_group_id"] for i in original_object["object_groups"]}
            # fake_data_config
            # Optional when it was created. 
            # If ori_fdc exists, add in "update_list", if it doesn't, add in "create_list" 
            if not original_fdc and data["fake_data_config"]:
                if data["fake_data_config"]["fake_data_config_base"]:
                    fdc_base["create_list"].append(self.fdcBase_operate.create_schemas(
                        **data["fake_data_config"]["fake_data_config_base"]))
                else:
                    fdc_base["create_list"].append(self.fdcBase_operate.create_schemas())
                fdc["create_list"].append(self.fdc_operate.create_schemas(
                    **data["fake_data_config"], object_id=original_object["id"]))
            elif original_fdc and data["fake_data_config"]:
                if data["fake_data_config"]["fake_data_config_base"]:
                    fdc_base["update_list"].append(self.fdcBase_operate.multiple_update_schemas(
                        **data["fake_data_config"]["fake_data_config_base"],
                        id=original_fdc["fake_data_config_base"]["id"]))
                fdc["update_list"].append(self.fdc_operate.multiple_update_schemas(
                    **data["fake_data_config"], id=original_fdc["id"]))
            # object_base
            # Not optional when created
            if data["object_base"]:
                o_base["update_list"].append(self.object_base_operate.multiple_update_schemas(
                    **data["object_base"], id=original_o_base["id"]))
            # object group
            for og in data["object_groups"]:
                if og in original_og:
                    continue
                elif og < 0:
                    oog["delete_og_ids"].add(-og)
                elif og > 0 and og not in original_og:
                    oog["create_list"].append(
                        self.oo_group_operate.create_schemas(object_id=data["id"], object_group_id=og))
            for _list in self.oo_group_operate.read_from_redis_by_key_set(oog["delete_og_ids"], 2):
                oog["delete_id_set"].update(_list)
            # object
            o["update_list"].append(self.object_operate.multiple_update_schemas(
                **data))
        # DB operate
        fdc_base["sql_list"].extend(self.fdcBase_operate.create_sql(db, fdc_base["create_list"]))
        # fdc create schemas add fdc_base_sql_data id
        for fdc_base_sql_data, create_data in zip(fdc_base["sql_list"], fdc["create_list"]):
            create_data.fake_data_config_base_id = fdc_base_sql_data.id
        fdc["sql_list"].extend(self.fdc_operate.create_sql(db, fdc["create_list"]))
        fdc_base["sql_list"].extend(self.fdcBase_operate.update_sql(db, fdc_base["update_list"]))
        fdc["sql_list"].extend(self.fdc_operate.update_sql(db, fdc["update_list"]))
        oog["sql_list"].extend(self.oo_group_operate.create_sql(db, oog["create_list"]))
        oog["delete_data_list"].extend(self.oo_group_operate.delete_sql(db, oog["delete_id_set"]))
        o_base["sql_list"].extend(self.object_base_operate.update_sql(db, o_base["update_list"]))
        o["sql_list"].extend(self.object_operate.update_sql(db, o["update_list"]))
        # redis operate
        # redis delete index table
        self.fdcBase_operate.delete_redis_index_table(
            [i["fake_data_config"]["fake_data_config_base"] for i in original_data_list
                if i["fake_data_config"]], fdc_base["update_list"])
        self.fdc_operate.delete_redis_index_table(
            [i["fake_data_config"] for i in original_data_list if i["fake_data_config"]], fdc["update_list"])
        self.object_base_operate.delete_redis_index_table(
            [i["object_base"] for i in original_data_list if i["object_base"]], o_base["update_list"])
        self.object_operate.delete_redis_index_table([i for i in original_data_list], o["update_list"])
        self.oo_group_operate.delete_redis_table(oog["delete_data_list"])
        # update redis table
        self.fdcBase_operate.update_redis_table(fdc_base["sql_list"])
        self.fdc_operate.update_redis_table(fdc["sql_list"])
        self.oo_group_operate.update_redis_table(oog["sql_list"])
        self.object_base_operate.update_redis_table(o_base["sql_list"])
        self.object_operate.update_redis_table(o["sql_list"])
        # reload related redis table
        self.oo_group_operate.reload_redis_table(
            db, self.oo_group_operate.reload_related_redis_tables, oog["sql_list"]+oog["delete_data_list"])
        self.object_operate.reload_redis_table(db, self.object_operate.reload_related_redis_tables,
                                                o["sql_list"], self_ref_id_dict)
        return o["sql_list"]


    def delete_multiple_object(self, id_set: set[int], db: Session):
        original_data_list = self.object_operate.read_from_redis_by_key_set(id_set)
        fdc = create_delete_dict()
        fdc_base = create_delete_dict()
        o = create_delete_dict()
        o_base = create_delete_dict()
        o["data_list"] = original_data_list
        for original_data in original_data_list:
            if original_data["fake_data_config"]:
                original_fdc = original_data["fake_data_config"]
                original_fdc_base = original_data["fake_data_config"]["fake_data_config_base"]
                fdc_base["id_set"].add(original_fdc_base["id"])
                fdc["id_set"].add(original_fdc["id"])
                fdc_base["data_list"].append(original_fdc_base)
                fdc["data_list"].append(original_fdc)
            original_o_base = original_data["object_base"]
            o["id_set"].add(original_data["id"])
            o_base["id_set"].add(original_o_base["id"])
            o_base["data_list"].append(original_o_base)
        # delete object_object_group
        try:
            oo_groups_id_list = self.oo_group_operate.read_from_redis_by_key_set_without_exception(o["id_set"], 1)
        except self.exc:
            oo_groups_id_list = []
        oo_groups_id_set = set()
        for ll in oo_groups_id_list:
            oo_groups_id_set |= set(ll)
        oo_groups_dict_list = self.oo_group_operate.read_from_redis_by_key_set(oo_groups_id_set)
        self.oo_group_operate.delete_sql(db, oo_groups_id_set, False)
        self.fdc_operate.delete_sql(db, fdc["id_set"], False)
        self.object_operate.delete_sql(db, o["id_set"], False)
        self.object_base_operate.delete_sql(db, o_base["id_set"], False)
        self.fdcBase_operate.delete_sql(db, fdc_base["id_set"], False)
        # delete redis_db table
        self.oo_group_operate.delete_redis_table(oo_groups_dict_list)
        self.fdcBase_operate.delete_redis_table(fdc_base["data_list"])
        self.fdc_operate.delete_redis_table(fdc["data_list"])
        self.object_base_operate.delete_redis_table(o_base["data_list"])
        self.object_operate.delete_redis_table(o["data_list"])
        # reload related redis_db table
        self.object_operate.reload_redis_table(
            db, self.object_operate.reload_related_redis_tables, original_data_list)
        self.oo_group_operate.reload_redis_table(
            db, self.oo_group_operate.reload_related_redis_tables, oo_groups_dict_list)

    def read_value_from_redis(self, id_set: set[int]) -> list[dict]:
        return self.read_redis_data_without_exception("object_value", id_set)

    def write_value_to_redis(self, mapping: dict):
        self.write_to_redis("object_value", mapping=mapping)

    def write_to_history(self, _id: str, uid: str, value: str):
        try:
            value2 = float(value)
            p = influxdb_client.Point(
                "object_value").tag("id", str(_id)) \
                .tag("uid", str(uid)) \
                .field("value", value2)
        except ValueError:
            value2 = str(value)
            p = influxdb_client.Point(
                "object_value").tag("id", str(_id)) \
                .tag("uid", str(uid)) \
                .field("value_string", value2)
        self.write(p)

    def query_history_by_id(self, start: str, stop: str, _id: str = "",
                            uid: str = "", skip: int = 0,
                            limit: int = None) -> list[dict]:
        stop_str = ""
        if stop:
            stop_str = f", stop: {stop}"
        id_str = ""
        if _id:
            id_str = f"""|> filter(fn:(r) => r.id == "{_id}")"""
        uid_str = ""
        if uid:
            uid_str = f"""|> filter(fn:(r) => r.uid == "{uid}")"""
        stmt = f'''from(bucket:"node_object")
|> range(start: {start}{stop_str})
|> filter(fn:(r) => r._measurement == "object_value")
{id_str}
{uid_str}'''
        d = self.query(stmt)
        result = []
        for table in d:
            for record in table.records:
                result.append(
                    {
                        "id": record.values.get("id"),
                        "uid": record.values.get("uid"),
                        "value": record.get_value(),
                        "timestamp": record.get_time().timestamp(),
                    }
                )
        if limit is not None:
            result = result[skip:skip + limit]
        else:
            result = result[skip:]
        return result
