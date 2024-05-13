import data.control_href_group
import data.control_href_item
from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.function.General_operate import GeneralOperate


class APIChgFunction:

    @staticmethod
    def format_simple_api_chg(chg: dict) -> dict:
        return {
            "id": chg["id"],
            "uid": chg["uid"]
        }


class APIControlHrefGroupOperate(GeneralOperate, APIChgFunction):
    def __init__(self, module, redis_db, influxdb: InfluxDB, exc):
        self.exc = exc
        GeneralOperate.__init__(self, module, redis_db, influxdb, exc)
        self.chg_operate = GeneralOperate(data.control_href_group, redis_db, influxdb, exc)
        self.chi_operate = GeneralOperate(data.control_href_item, redis_db, influxdb, exc)
