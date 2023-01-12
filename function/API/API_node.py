from sqlalchemy.orm import Session

from function.API.API_object import APIObjectOperate
from function.General_operate import GeneralOperate
import data.node
import data.node_base
import data.third_dimension_instance
import data.device_info
import data.node_node_group
import data.object
import data.API.API_object
from function.create_data_structure import create_delete_dict


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
            "uid": node["node_id"],
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
    def __init__(self, module, redis_db, exc):
        self.exc = exc
        GeneralOperate.__init__(self, module, redis_db, exc)
        self.node_operate = GeneralOperate(data.node, redis_db, exc)
        self.node_base_operate = GeneralOperate(data.node_base, redis_db, exc)
        self.third_d_operate = GeneralOperate(data.third_dimension_instance, redis_db, exc)
        self.device_info_operate = GeneralOperate(data.device_info, redis_db, exc)
        self.nn_group_operate = GeneralOperate(data.node_node_group, redis_db, exc)
        self.object_operate = GeneralOperate(data.object, redis_db, exc)
        self.api_object_operate = APIObjectOperate(data.API.API_object, redis_db, exc)

    def get_delete_data(self, node_id_set: set, result=None) -> dict[str, dict]:
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
        if not node_id_set:
            return result

        # delete duplicate from button stack
        duplicate = node_id_set & result["node"]["set"]
        add_node_set = node_id_set - (node_id_set & result["node"]["set"])
        if duplicate:
            for s in result["node"]["stack"]:
                u = s & duplicate
                if u:
                    s -= u
                    duplicate -= u
                    if not duplicate:
                        break

        result["node"]["stack"].append(node_id_set)
        node_data_list = self.node_operate.read_data_from_redis_by_key_set(node_id_set)
        child_id_set = self.get_child_node(node_data_list)
        try:
            nn_groups_id_list = self.nn_group_operate.read_data_from_redis_by_key_set(add_node_set, 1)
        except self.exc:
            nn_groups_id_list = []
        nn_groups_id_set = set()
        for ll in nn_groups_id_list:
            nn_groups_id_set |= set(ll)
        result["nn_group"]["id_set"] |= set(nn_groups_id_set)
        result["nn_group"]["data_list"].extend(
            self.nn_group_operate.read_data_from_redis_by_key_set(nn_groups_id_set))
        result = self.get_set(node_data_list, result)
        result["node"]["set"] |= node_id_set
        return self.get_delete_data(child_id_set, result)

    def delete_nodes(self, db: Session, id_set: set[int]):
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
