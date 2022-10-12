from node_object_function.API.API_object import APIObjectOperate
from node_object_function.General_operate import GeneralOperate
import node_object_data.node
import node_object_data.node_base
import node_object_data.third_dimension_instance
import node_object_data.device_info
import node_object_data.node_node_group
import node_object_data.object
import node_object_data.API.API_object
from node_object_function.create_data_structure import create_delete_dict


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


class APINodeOperate(GeneralOperate, APINodeFunction):
    def __init__(self, module, redis_db, exc):
        self.exc = exc
        GeneralOperate.__init__(self, module, redis_db, exc)
        self.node_operate = GeneralOperate(node_object_data.node, redis_db, exc)
        self.node_base_operate = GeneralOperate(node_object_data.node_base, redis_db, exc)
        self.third_d_operate = GeneralOperate(node_object_data.third_dimension_instance, redis_db, exc)
        self.device_info_operate = GeneralOperate(node_object_data.device_info, redis_db, exc)
        self.nn_group_operate = GeneralOperate(node_object_data.node_node_group, redis_db, exc)
        self.object_operate = GeneralOperate(node_object_data.object, redis_db, exc)
        self.api_object_operate = APIObjectOperate(node_object_data.API.API_object, redis_db, exc)

    @staticmethod
    def __get_set(node_data_list: list, result: dict) -> tuple:
        child_id_set = set()
        for data in node_data_list:
            node_base = data["node_base"]
            tdi = data["third_dimension_instance"]
            for item in data["child_nodes"]:
                child_id_set.add(item["id"])
            for item in data["objects"]:
                result["object"]["id_set"].add(item["id"])
            result["node_base"]["id_set"].add(node_base["id"])
            result["node_base"]["data_list"].append(node_base)
            if node_base["device_info"]:
                result["device_info"]["id_set"].add(node_base["device_info"]["id"])
                result["device_info"]["data_list"].append(node_base["device_info"])
            if tdi:
                result["tdi"]["id_set"].add(data["third_dimension_instance"]["id"])
                result["tdi"]["data_list"].append(data["third_dimension_instance"])
        return child_id_set, result

    def get_delete_data(self, node_id_set: set, result=None):
        if result is None:
            result = {
                "node": {
                    "data_list": [],
                    "stack": []
                },
                "tdi": create_delete_dict(),
                "device_info": create_delete_dict(),
                "node_base": create_delete_dict(),
                "nn_group": create_delete_dict(),
                "object": create_delete_dict(),
            }
        if not node_id_set:
            return result
        node_data_list = self.node_operate.read_data_from_redis_by_key_set(node_id_set)
        result["node"]["stack"].append(node_id_set)
        try:
            nn_groups_id_list = self.nn_group_operate.read_data_from_redis_by_key_set(node_id_set, 1)
        except self.exc:
            nn_groups_id_list = []
        nn_groups_id_set = set()
        for ll in nn_groups_id_list:
            nn_groups_id_set |= set(ll)
        result["nn_group"]["id_set"] |= set(nn_groups_id_set)
        result["nn_group"]["data_list"].extend(
            self.nn_group_operate.read_data_from_redis_by_key_set(nn_groups_id_set))
        result["node"]["data_list"].extend(node_data_list)
        child_id_set, result = self.__get_set(node_data_list, result)
        return self.get_delete_data(child_id_set, result)
