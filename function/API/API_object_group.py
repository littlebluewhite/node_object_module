from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.function.General_operate import GeneralOperate
import data.node
import data.node_group
import data.node_node_group
import data.object
import data.object_group
import data.object_object_group


class APIObjectGroupFunction:
    @staticmethod
    def format_object_group_and_objects(object_group_data: dict):
        _object_list = list()
        for object in object_group_data.get("objects"):
            _object_list.append(object.get("object_id"))
        _object_list.sort()
        object_group_data["objects"] = _object_list
        return object_group_data


class APIObjectGroupOperate(GeneralOperate, APIObjectGroupFunction):
    def __init__(self, module, redis_db, influxdb: InfluxDB, exc):
        self.exc = exc
        self.object_operate = GeneralOperate(data.object, redis_db, influxdb, exc)
        self.object_group_operate = GeneralOperate(data.object_group, redis_db, influxdb, exc)
        self.object_object_group_operate = GeneralOperate(data.object_object_group, redis_db, influxdb, exc)
        GeneralOperate.__init__(self, module, redis_db, influxdb, exc)
