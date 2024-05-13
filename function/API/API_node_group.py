from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.function.General_operate import GeneralOperate
import data.node
import data.node_group
import data.node_node_group

class APINodeGroupFunction:
    @staticmethod
    def format_node_group_and_nodes(node_group_data: dict):
        _node_list = list()
        for node in node_group_data.get("nodes"):
            _node_list.append(node.get("node_id"))
        _node_list.sort()
        node_group_data["nodes"] = _node_list
        return node_group_data
    
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


class APINodeGroupOperate(GeneralOperate, APINodeGroupFunction):
    def __init__(self, module, redis_db, influxdb: InfluxDB, exc):
        self.exc = exc
        self.node_operate = GeneralOperate(data.node, redis_db, influxdb, exc)
        self.node_group_operate = GeneralOperate(data.node_group, redis_db, influxdb, exc)
        self.node_node_group_operate = GeneralOperate(data.node_node_group, redis_db, influxdb, exc)
        GeneralOperate.__init__(self, module, redis_db, influxdb, exc)
    