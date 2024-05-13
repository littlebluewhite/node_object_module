from sqlalchemy.orm import Session

from function.API.API_object import APIObjectOperate
from general_operator.function.General_operate import GeneralOperate
import data.node
import data.node_base
import data.third_dimension_instance
import data.device_info
import data.node_node_group
import data.object
import data.API.API_object
import data.node_group
from general_operator.function.create_data_structure import create_delete_dict, create_update_dict
from schemas.API.API_node import APINodeMultipleUpdate
from schemas.API.API_object import APIObjectMultipleUpdate


class APINodeFunction:
    @staticmethod
    def format_api_node(node: dict):
        child_nodes = []
        node_groups = []
        objects = []
        for item in node["child_nodes"]:
            child_nodes.append(item["id"])
        for item in node["node_groups"]:
            node_groups.append(item["node_group_id"])
        for item in node["objects"]:
            objects.append(item["id"])
        node["child_nodes"] = child_nodes
        node["node_groups"] = node_groups
        node["objects"] = objects
        return node

    @staticmethod
    def format_simple_api_node(node: dict) -> dict:
        return {
            "id": node["id"],
            "uid": node["uid"],
            "name": node["node_base"]["name"]
        }

    @staticmethod
    def get_child_node(node_data_list: list) -> set[int]:
        child_id_set = set()
        for d in node_data_list:
            for item in d["child_nodes"]:
                child_id_set.add(item["id"])
        return child_id_set

    @staticmethod
    def get_set(node_data_list: list, result: dict) -> dict:
        for d in node_data_list:
            if d["id"] not in result["node"]["set"]:
                result["node"]["data_list"].append(d)
                node_base = d["node_base"]
                tdi = d["third_dimension_instance"]
                for item in d["objects"]:
                    result["object"]["id_set"].add(item["id"])
                result["node_base"]["id_set"].add(node_base["id"])
                result["node_base"]["data_list"].append(node_base)
                if node_base["device_info"]:
                    result["device_info"]["id_set"].add(node_base["device_info"]["id"])
                    result["device_info"]["data_list"].append(node_base["device_info"])
                if tdi:
                    result["tdi"]["id_set"].add(d["third_dimension_instance"]["id"])
                    result["tdi"]["data_list"].append(d["third_dimension_instance"])
        return result


class APINodeOperate(GeneralOperate, APINodeFunction):
    def __init__(self, module, redis_db, influxdb, exc):
        self.exc = exc
        GeneralOperate.__init__(self, module, redis_db, influxdb, exc)
        self.node_operate = GeneralOperate(data.node, redis_db, influxdb, exc)
        self.node_group_operate = GeneralOperate(data.node_group, redis_db, influxdb, exc)
        self.node_base_operate = GeneralOperate(data.node_base, redis_db, influxdb, exc)
        self.third_d_operate = GeneralOperate(data.third_dimension_instance, redis_db, influxdb, exc)
        self.device_info_operate = GeneralOperate(data.device_info, redis_db, influxdb, exc)
        self.nn_group_operate = GeneralOperate(data.node_node_group, redis_db, influxdb, exc)
        self.object_operate = GeneralOperate(data.object, redis_db, influxdb, exc)
        self.api_object_operate = APIObjectOperate(data.API.API_object, redis_db, influxdb, exc)

    def get_delete_data(self, id_set: set, result=None) -> dict[str, dict]:
        if result is None:
            result = {
                "node": {
                    "data_list": [],
                    "stack": [],
                    # multiple delete check duplicate
                    "set": set(),
                },
                "tdi": create_delete_dict(),
                "device_info": create_delete_dict(),
                "node_base": create_delete_dict(),
                "nn_group": create_delete_dict(),
                "object": create_delete_dict(),
            }
        if not id_set:
            return result

        # delete duplicate from button stack
        duplicate = id_set & result["node"]["set"]
        add_node_set = id_set - (id_set & result["node"]["set"])
        if duplicate:
            for s in result["node"]["stack"]:
                u = s & duplicate
                if u:
                    s -= u
                    duplicate -= u
                    if not duplicate:
                        break

        result["node"]["stack"].append(id_set)
        node_data_list = self.node_operate.read_from_redis_by_key_set(id_set)
        child_id_set = self.get_child_node(node_data_list)
        nn_groups_id_list = self.nn_group_operate.read_from_redis_by_key_set_without_exception(add_node_set, 1)

        nn_groups_id_set = set()
        for ll in nn_groups_id_list:
            nn_groups_id_set |= set(ll)
        result["nn_group"]["id_set"] |= set(nn_groups_id_set)
        result["nn_group"]["data_list"].extend(
            self.nn_group_operate.read_from_redis_by_key_set(nn_groups_id_set))
        result = self.get_set(node_data_list, result)
        result["node"]["set"] |= id_set
        return self.get_delete_data(child_id_set, result)

    def update_multiple_node(self, update_list: list[APINodeMultipleUpdate], db: Session):
        update_dict_list = [i.dict() for i in update_list]
        nng = create_update_dict(delete=True)
        nng["delete_ng_ids"] = set()
        device = create_update_dict()
        tdi = create_update_dict()
        node = create_update_dict(create=False)
        node_base = create_update_dict(create=False)
        original_data_list = self.node_operate.read_from_redis_by_key_set({i.id for i in update_list})
        original_key_id_dict: dict = {i["id"]: i for i in original_data_list}
        self_ref_id_dict: dict = self.node_operate.get_self_ref_id(
            [self.node_operate.main_schemas(**i) for i in original_data_list])
        # deal with update data
        for data in update_dict_list:
            original_node: dict = original_key_id_dict[data["id"]]
            original_node_base: dict = original_node["node_base"]
            original_device = original_node_base["device_info"]
            original_tdi = original_node["third_dimension_instance"]
            original_ng: set = {i["node_group_id"] for i in original_node["node_groups"]}
            # node_base
            if data["node_base"]:
                # node_base["update_list"].append(self.node_base_operate.multiple_update_schemas(
                #     **data))
                node_base["update_list"].append(self.node_base_operate.multiple_update_schemas(
                    id=data["id"], **data["node_base"]))
                # device_info
                if not original_device and data["node_base"]["device_info"]:
                    device["create_list"].append(self.device_info_operate.create_schemas(
                        **data["node_base"]["device_info"],
                        node_base_id=original_node_base["id"]))
                elif original_device and data["node_base"]["device_info"]:
                    original_device["update_list"].append(self.device_info_operate.multiple_update_schemas(
                        **data["node_base"]["device_info"]))
            # third_dimension_instance
            if not original_tdi and data["third_dimension_instance"]:
                tdi["create_list"].append(self.third_d_operate.create_schemas(
                    **data["third_dimension_instance"],
                    node_id=data["id"]))
            elif original_tdi and data["third_dimension_instance"]:
                tdi["update_list"].append(self.third_d_operate.multiple_update_schemas(
                    **data["third_dimension_instance"], id=original_tdi["id"]))
            # node group
            for ng in data.get("node_groups"):
                if ng in original_ng:
                    continue
                elif ng < 0:
                    nng["delete_ng_ids"].add(-ng)
                elif ng > 0 and ng not in original_ng:
                    nng["create_list"].append(
                        self.nn_group_operate.create_schemas(node_id=data["id"], node_group_id=ng))
            for _list in self.nn_group_operate.read_from_redis_by_key_set(nng["delete_ng_ids"], 2):
                nng["delete_id_set"].update(_list)
            # node
            node["update_list"].append(self.node_operate.multiple_update_schemas(**data))
        # DB operate
        device["sql_list"].extend(self.device_info_operate.create_sql(db, device["create_list"]))
        device["sql_list"].extend(self.device_info_operate.update_sql(db, device["update_list"]))
        tdi["sql_list"].extend(self.third_d_operate.create_sql(db, tdi["create_list"]))
        tdi["sql_list"].extend(self.third_d_operate.update_sql(db, tdi["update_list"]))
        nng["sql_list"].extend(self.nn_group_operate.create_sql(db, nng["create_list"]))
        nng["delete_data_list"].extend(self.nn_group_operate.delete_sql(db, nng["delete_id_set"]))
        node_base["sql_list"].extend(self.node_base_operate.update_sql(db, node_base["update_list"]))
        node["sql_list"].extend(self.node_operate.update_sql(db, node["update_list"]))
        # redis operate
        # delete redis index table
        self.device_info_operate.delete_redis_index_table(
            [i["node_base"]["device_info"] for i in original_data_list if i["node_base"]["device_info"]],
            device["update_list"])
        self.third_d_operate.delete_redis_index_table(
            [i["third_dimension_instance"] for i in original_data_list if i["third_dimension_instance"]],
            tdi["update_list"])
        self.node_base_operate.delete_redis_index_table(
            [i["node_base"] for i in original_data_list if i["node_base"]],
            node_base["update_list"])
        self.node_operate.delete_redis_index_table([i for i in original_data_list], node["update_list"])
        # delete redis table
        self.nn_group_operate.delete_redis_table(nng["delete_data_list"])
        # update redis table
        self.device_info_operate.update_redis_table(device["sql_list"])
        self.third_d_operate.update_redis_table(tdi["sql_list"])
        self.nn_group_operate.update_redis_table(nng["sql_list"])
        self.node_base_operate.update_redis_table(node_base["sql_list"])
        self.node_operate.update_redis_table(node["sql_list"])
        # reload related redis table
        self.nn_group_operate.reload_redis_table(
            db, self.nn_group_operate.reload_related_redis_tables, nng["sql_list"] + nng["delete_data_list"])
        self.node_operate.reload_redis_table(
            db, self.node_operate.reload_related_redis_tables, node["sql_list"], self_ref_id_dict)
        return node["sql_list"]

    def delete_nodes_including_object(self, db: Session, id_set: set[int]):
        delete_data = self.get_delete_data(id_set)
        print("delete_data: ", delete_data)
        self.api_object_operate.delete_multiple_object(delete_data["object"]["id_set"], db)
        self.nn_group_operate.delete_sql(db, delete_data["nn_group"]["id_set"], False)
        self.third_d_operate.delete_sql(db, delete_data["tdi"]["id_set"], False)
        self.device_info_operate.delete_sql(db, delete_data["device_info"]["id_set"], False)
        while delete_data["node"]["stack"]:
            id_set = delete_data["node"]["stack"].pop()
            self.node_operate.delete_sql(db, id_set, False)
        self.node_base_operate.delete_sql(db, delete_data["node_base"]["id_set"], False)
        # delete redis_db table
        self.nn_group_operate.delete_redis_table(delete_data["nn_group"]["data_list"])
        self.third_d_operate.delete_redis_table(delete_data["tdi"]["data_list"])
        self.device_info_operate.delete_redis_table(delete_data["device_info"]["data_list"])
        self.node_operate.delete_redis_table(delete_data["node"]["data_list"])
        self.node_base_operate.delete_redis_table(delete_data["node_base"]["data_list"])
        # reload related redis_db table
        self.nn_group_operate.reload_redis_table(
            db, self.nn_group_operate.reload_related_redis_tables, delete_data["nn_group"]["data_list"])
        self.node_operate.reload_redis_table(
            db, self.node_operate.reload_related_redis_tables, delete_data["node"]["data_list"])
        return "ok"

    def delete_nodes_excluding_object(self, db: Session, id_set: set[int]):
        delete_data = self.get_delete_data(id_set)
        print("delete_data: ", delete_data)
        # self.api_object_operate.delete_multiple_object(delete_data["object"]["id_set"], db)
        upt_obj: list[APIObjectMultipleUpdate] = [self.api_object_operate.multiple_update_schemas(
            id=_id, node_id="") for _id in delete_data["object"]["id_set"]]
        self.api_object_operate.update_multiple_object(upt_obj, db)

        self.nn_group_operate.delete_sql(db, delete_data["nn_group"]["id_set"], False)
        self.third_d_operate.delete_sql(db, delete_data["tdi"]["id_set"], False)
        self.device_info_operate.delete_sql(db, delete_data["device_info"]["id_set"], False)
        while delete_data["node"]["stack"]:
            id_set = delete_data["node"]["stack"].pop()
            self.node_operate.delete_sql(db, id_set, False)
        self.node_base_operate.delete_sql(db, delete_data["node_base"]["id_set"], False)
        # delete redis_db table
        self.nn_group_operate.delete_redis_table(delete_data["nn_group"]["data_list"])
        self.third_d_operate.delete_redis_table(delete_data["tdi"]["data_list"])
        self.device_info_operate.delete_redis_table(delete_data["device_info"]["data_list"])
        self.node_operate.delete_redis_table(delete_data["node"]["data_list"])
        self.node_base_operate.delete_redis_table(delete_data["node_base"]["data_list"])
        # reload related redis_db table
        self.nn_group_operate.reload_redis_table(
            db, self.nn_group_operate.reload_related_redis_tables, delete_data["nn_group"]["data_list"])
        self.node_operate.reload_redis_table(
            db, self.node_operate.reload_related_redis_tables, delete_data["node"]["data_list"])
        return "ok"
