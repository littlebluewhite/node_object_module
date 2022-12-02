from sqlalchemy.orm import Session

import data.object
import data.object_base
import data.object_object_group
import data.fake_data_config
import data.fake_data_config_base
from function.General_operate import GeneralOperate
from function.create_data_structure import create_delete_dict


class APIObjectFunction:
    @staticmethod
    def format_api_object(obj: dict):
        object_groups = []
        for item in obj["object_groups"]:
            object_groups.append(item["object_group_id"])
        obj["object_groups"] = object_groups
        return obj


class APIObjectOperate(GeneralOperate):
    def __init__(self, module, redis_db, exc):
        self.exc = exc
        self.insert_schemas = module.insert_schemas
        self.get_value_schemas = module.get_value_schemas
        GeneralOperate.__init__(self, module, redis_db, exc)
        self.object_operate = GeneralOperate(data.object, redis_db, exc)
        self.object_base_operate = GeneralOperate(data.object_base, redis_db, exc)
        self.oo_groups_operate = GeneralOperate(data.object_object_group, redis_db, exc)
        self.fdc_operate = GeneralOperate(data.fake_data_config, redis_db, exc)
        self.fdcBase_operate = GeneralOperate(data.fake_data_config_base, redis_db, exc)

    def delete_multiple_object(self, id_set: set[int], db: Session):
        original_data_list = self.object_operate.read_data_from_redis_by_key_set(id_set)
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
            oo_groups_id_list = self.oo_groups_operate.read_data_from_redis_by_key_set(o["id_set"], 1)
        except self.exc:
            oo_groups_id_list = []
        oo_groups_id_set = set()
        for ll in oo_groups_id_list:
            oo_groups_id_set |= set(ll)
        oo_groups_dict_list = self.oo_groups_operate.read_data_from_redis_by_key_set(oo_groups_id_set)
        self.oo_groups_operate.delete_sql(db, oo_groups_id_set, False)
        self.fdc_operate.delete_sql(db, fdc["id_set"], False)
        self.object_operate.delete_sql(db, o["id_set"], False)
        self.object_base_operate.delete_sql(db, o_base["id_set"], False)
        self.fdcBase_operate.delete_sql(db, fdc_base["id_set"], False)
        # delete redis_db table
        self.oo_groups_operate.delete_redis_table(oo_groups_dict_list)
        self.fdcBase_operate.delete_redis_table(fdc_base["data_list"])
        self.fdc_operate.delete_redis_table(fdc["data_list"])
        self.object_base_operate.delete_redis_table(o_base["data_list"])
        self.object_operate.delete_redis_table(o["data_list"])
        # reload related redis_db table
        self.object_operate.reload_redis_table(
            db, self.object_operate.reload_related_redis_tables, original_data_list)
        self.oo_groups_operate.reload_redis_table(
            db, self.oo_groups_operate.reload_related_redis_tables, oo_groups_dict_list)
